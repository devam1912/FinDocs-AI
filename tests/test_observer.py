import os
import json
import sqlite3
import pytest
from src.observer import AgentSubject, AgentObserver, FileLoggingObserver, SQLiteLoggingObserver
from src.agent import QueryContext

class MockObserver(AgentObserver):
    def __init__(self):
        self.called = False
        self.context_received = None
        
    def update(self, context) -> None:
        self.called = True
        self.context_received = context

def test_subject_observer_detachment():
    # Arrange
    subject = AgentSubject()
    observer = MockObserver()
    context = QueryContext("test query")
    
    # Act
    subject.attach(observer)
    subject.notify(context)
    
    # Assert
    assert observer.called is True
    assert observer.context_received == context
    
    # Detach and notify again
    observer.called = False
    subject.detach(observer)
    subject.notify(context)
    assert observer.called is False

def test_file_logging_observer(tmp_path):
    # Arrange
    log_file = tmp_path / "interactions.jsonl"
    observer = FileLoggingObserver(log_filepath=str(log_file))
    
    context = QueryContext("How much is Netflix?")
    context.intent = "RETRIEVAL"
    context.tool_to_use = "semantic_retrieval_tool"
    context.final_response = "Netflix is $15.49"
    context.metadata["total_latency"] = 1.25
    
    # Act
    observer.update(context)
    
    # Assert
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == 1
        data = json.loads(lines[0])
        assert data["query"] == "How much is Netflix?"
        assert data["intent"] == "RETRIEVAL"
        assert data["tool_used"] == "semantic_retrieval_tool"
        assert data["response"] == "Netflix is $15.49"
        assert data["latency"] == 1.25
        assert data["success"] is True

def test_sqlite_logging_observer(tmp_path):
    # Arrange
    db_file = tmp_path / "logs.db"
    observer = SQLiteLoggingObserver(db_path=str(db_file))
    
    context = QueryContext("What was my spend in March?")
    context.intent = "STRUCTURED_SQL"
    context.tool_to_use = "structured_database_tool"
    context.final_response = "You spent $2,243.83"
    context.metadata["total_latency"] = 0.85
    
    # Act
    observer.update(context)
    
    # Assert
    assert os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM agent_logs;")
    rows = cursor.fetchall()
    conn.close()
    
    assert len(rows) == 1
    row = rows[0]
    # columns order: id, timestamp, query, intent, tool_used, success, latency, response, error
    assert row[2] == "What was my spend in March?"
    assert row[3] == "STRUCTURED_SQL"
    assert row[4] == "structured_database_tool"
    assert row[5] == 1
    assert row[6] == 0.85
    assert row[7] == "You spent $2,243.83"
    assert row[8] is None
