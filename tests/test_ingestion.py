import os
import pytest
from src.ingestion import parse_csv, parse_pdf

def test_parse_csv():
    # Arrange
    csv_file = "data/statement_2026_01.csv"
    assert os.path.exists(csv_file), "Mock CSV data file must exist to run tests."
    
    # Act
    transactions = parse_csv(csv_file)
    
    # Assert
    assert len(transactions) == 14
    first_tx = transactions[0]
    assert first_tx["Date"] == "2026-01-01"
    assert first_tx["Description"] == "TechCorp Salary"
    assert first_tx["Category"] == "Income"
    assert first_tx["Amount"] == 5000.0
    assert first_tx["source_file"] == "statement_2026_01.csv"

def test_parse_pdf():
    # Arrange
    pdf_file = "data/statement_2026_03.pdf"
    assert os.path.exists(pdf_file), "Mock PDF data file must exist to run tests."
    
    # Act
    transactions = parse_pdf(pdf_file)
    
    # Assert
    assert len(transactions) == 14
    first_tx = transactions[0]
    assert first_tx["Date"] == "2026-03-01"
    assert first_tx["Description"] == "TechCorp Salary"
    assert first_tx["Category"] == "Income"
    assert first_tx["Amount"] == 5000.0
    assert first_tx["source_file"] == "statement_2026_03.pdf"
