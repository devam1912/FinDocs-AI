import os
import re
import csv
import sqlite3
import pypdf
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_mistralai import MistralAIEmbeddings

# Import configurations
try:
    from src.config import MISTRAL_API_KEY, DATABASE_PATH, VECTOR_STORE_PATH
except ImportError:
    # Handle direct scripts execution
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import MISTRAL_API_KEY, DATABASE_PATH, VECTOR_STORE_PATH

def parse_csv(filepath: str) -> list[dict]:
    """Parse a CSV bank statement and return a list of transactions."""
    transactions = []
    basename = os.path.basename(filepath)
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                transactions.append({
                    "Date": row["Date"],
                    "Description": row["Description"],
                    "Category": row["Category"],
                    "Amount": float(row["Amount"]),
                    "source_file": basename
                })
            except (ValueError, KeyError) as e:
                print(f"Skipping row in {basename} due to parsing error: {row}. Error: {e}")
    return transactions

def parse_pdf(filepath: str) -> list[dict]:
    """Parse a PDF bank statement and return a list of transactions."""
    transactions = []
    basename = os.path.basename(filepath)
    
    reader = pypdf.PdfReader(filepath)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
            
    lines = [line.strip() for line in full_text.split("\n") if line.strip()]
    
    i = 0
    while i < len(lines):
        # Match YYYY-MM-DD format
        if re.match(r"^\d{4}-\d{2}-\d{2}$", lines[i]):
            if i + 3 < len(lines):
                date = lines[i]
                desc = lines[i+1]
                cat = lines[i+2]
                amt_str = lines[i+3]
                
                # Format amount: e.g. "$5,000.00" -> 5000.0, "-$1,500.00" -> -1500.0
                clean_amt = amt_str.replace("$", "").replace(",", "")
                try:
                    amount = float(clean_amt)
                    transactions.append({
                        "Date": date,
                        "Description": desc,
                        "Category": cat,
                        "Amount": amount,
                        "source_file": basename
                    })
                except ValueError:
                    print(f"Skipping row in {basename} due to invalid amount format: {amt_str}")
                i += 4
            else:
                i += 1
        else:
            i += 1
            
    return transactions

def initialize_sqlite(db_path: str):
    """Initialize the SQLite database schema."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            source_file TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_to_sqlite(db_path: str, transactions: list[dict]):
    """Save transactions to SQLite database without duplicates."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    inserted_count = 0
    for tx in transactions:
        # Prevent exact duplicates
        cursor.execute("""
            SELECT COUNT(*) FROM transactions 
            WHERE date = ? AND description = ? AND category = ? AND amount = ? AND source_file = ?
        """, (tx["Date"], tx["Description"], tx["Category"], tx["Amount"], tx["source_file"]))
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO transactions (date, description, category, amount, source_file)
                VALUES (?, ?, ?, ?, ?)
            """, (tx["Date"], tx["Description"], tx["Category"], tx["Amount"], tx["source_file"]))
            inserted_count += 1
            
    conn.commit()
    conn.close()
    print(f"Inserted {inserted_count} new transactions into SQLite ({db_path})")

def save_to_vectorstore(vectorstore_path: str, transactions: list[dict], api_key: str):
    """Format transactions, generate embeddings, and save to FAISS index."""
    if not api_key:
        raise ValueError("MISTRAL_API_KEY is not set. Cannot run embeddings generation.")
        
    print(f"Generating embeddings and saving FAISS index to {vectorstore_path}...")
    embeddings = MistralAIEmbeddings(
        mistral_api_key=api_key,
        model="mistral-embed"
    )
    
    documents = []
    for tx in transactions:
        # Create a descriptive text chunk
        content = f"On {tx['Date']}, transaction for \"{tx['Description']}\" under category \"{tx['Category']}\" occurred for amount ${tx['Amount']:,.2f}."
        doc = Document(
            page_content=content,
            metadata={
                "date": tx["Date"],
                "description": tx["Description"],
                "category": tx["Category"],
                "amount": tx["Amount"],
                "source": tx["source_file"]
            }
        )
        documents.append(doc)
        
    if not documents:
        print("No transactions to index in vector store.")
        return
        
    vectorstore = FAISS.from_documents(documents, embeddings)
    os.makedirs(os.path.dirname(vectorstore_path), exist_ok=True)
    vectorstore.save_local(vectorstore_path)
    print("Vector store saved successfully.")

def run_ingestion_pipeline():
    """Main execution of the ingestion pipeline."""
    data_dir = "data"
    
    # 1. Parse all files
    all_transactions = []
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' does not exist. Please run mock data generation first.")
        return
        
    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if filename.endswith(".csv"):
            print(f"Parsing CSV statement: {filename}")
            txs = parse_csv(filepath)
            all_transactions.extend(txs)
            print(f"Parsed {len(txs)} transactions.")
        elif filename.endswith(".pdf"):
            print(f"Parsing PDF statement: {filename}")
            txs = parse_pdf(filepath)
            all_transactions.extend(txs)
            print(f"Parsed {len(txs)} transactions.")
            
    print(f"\nTotal parsed transactions: {len(all_transactions)}")
    
    # 2. SQLite Ingestion
    initialize_sqlite(DATABASE_PATH)
    save_to_sqlite(DATABASE_PATH, all_transactions)
    
    # 3. Vector store Ingestion
    save_to_vectorstore(VECTOR_STORE_PATH, all_transactions, MISTRAL_API_KEY)
    
    print("\nIngestion pipeline execution complete!")

if __name__ == "__main__":
    run_ingestion_pipeline()
