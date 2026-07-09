import os
import json
import sqlite3
import datetime
from abc import ABC, abstractmethod

# Import configurations
try:
    from src.config import DATABASE_PATH
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import DATABASE_PATH

class AgentObserver(ABC):
    """Abstract Observer class for monitoring agent interactions."""
    @abstractmethod
    def update(self, context) -> None:
        """Called when the Agent Subject notifies its observers of an interaction."""
        pass

class AgentSubject:
    """Subject class (Publisher) that maintains observers and dispatches updates."""
    def __init__(self):
        self._observers = []
        
    def attach(self, observer: AgentObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            
    def detach(self, observer: AgentObserver) -> None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
            
    def notify(self, context) -> None:
        for observer in self._observers:
            try:
                observer.update(context)
            except Exception as e:
                print(f"Error notifying observer {observer.__class__.__name__}: {e}")

class FileLoggingObserver(AgentObserver):
    """Observer that logs agent interactions to a local JSON Lines (JSONL) file."""
    def __init__(self, log_filepath: str = "logs/agent_interactions.jsonl"):
        self.log_filepath = log_filepath
        os.makedirs(os.path.dirname(self.log_filepath), exist_ok=True)
        
    def update(self, context) -> None:
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "query": context.query,
            "intent": context.intent,
            "tool_used": context.tool_to_use,
            "success": context.success,
            "latency": context.metadata.get("total_latency", 0),
            "response": context.final_response,
            "error": context.error
        }
        with open(self.log_filepath, mode="a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

class SQLiteLoggingObserver(AgentObserver):
    """Observer that logs agent interactions to an 'agent_logs' SQLite table."""
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self._initialize_table()
        
    def _initialize_table(self) -> None:
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                query TEXT NOT NULL,
                intent TEXT,
                tool_used TEXT,
                success INTEGER NOT NULL,
                latency REAL NOT NULL,
                response TEXT,
                error TEXT
            )
        """)
        conn.commit()
        conn.close()
        
    def update(self, context) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agent_logs (timestamp, query, intent, tool_used, success, latency, response, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.datetime.now().isoformat(),
            context.query,
            context.intent,
            context.tool_to_use,
            1 if context.success else 0,
            context.metadata.get("total_latency", 0),
            context.final_response,
            context.error
        ))
        conn.commit()
        conn.close()
