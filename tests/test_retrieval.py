import pytest
from langchain_core.documents import Document
from src.retrieval import retrieve_documents

def test_retrieve_documents_type():
    # Act
    docs = retrieve_documents("Netflix", k=1)
    
    # Assert
    assert isinstance(docs, list)
    assert len(docs) == 1
    assert isinstance(docs[0], Document)
    assert "Netflix" in docs[0].page_content

def test_retrieve_documents_metadata():
    # Act
    docs = retrieve_documents("Whole Foods Market", k=2)
    
    # Assert
    assert len(docs) >= 1
    doc = docs[0]
    assert "Whole Foods" in doc.page_content or "Whole Foods" in doc.metadata.get("description", "")
    assert "category" in doc.metadata
    assert doc.metadata["category"] == "Groceries"
    assert "amount" in doc.metadata
    assert doc.metadata["amount"] < 0
