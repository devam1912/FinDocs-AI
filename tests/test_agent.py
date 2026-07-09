import pytest
from src.agent import run_agent

def test_agent_structured_route():
    # Act
    ctx = run_agent("What is my total spending in March?")
    
    # Assert
    assert ctx.success is True
    assert ctx.intent == "STRUCTURED_SQL"
    assert ctx.tool_to_use == "structured_database_tool"
    assert ctx.final_response is not None
    assert "2,243.83" in ctx.final_response

def test_agent_retrieval_route():
    # Act
    ctx = run_agent("find the transaction for Spotify Premium")
    
    # Assert
    assert ctx.success is True
    assert ctx.intent == "RETRIEVAL"
    assert ctx.tool_to_use == "semantic_retrieval_tool"
    assert ctx.final_response is not None
    assert "Spotify" in ctx.final_response
