import os
import re
import sys
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from src.config import DATABASE_PATH
    from src.llm_strategy import get_llm_provider
except ImportError:
    # Handle direct script executions
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import DATABASE_PATH
    from src.llm_strategy import get_llm_provider

def get_sqlite_schema(db_path: str) -> str:
    """Retrieve schema definitions and metadata of the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    schema_parts = []
    for table_tuple in tables:
        table_name = table_tuple[0]
        if table_name == "sqlite_sequence":
            continue
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        create_sql = cursor.fetchone()[0]
        schema_parts.append(create_sql)
        
        # If it's the transactions table, append distinct categories to guide the LLM
        if table_name == "transactions":
            try:
                cursor.execute("SELECT DISTINCT category FROM transactions;")
                categories = [row[0] for row in cursor.fetchall() if row[0]]
                schema_parts.append(f"-- Distinct categories in transactions table: {categories}")
            except Exception:
                pass
        
    conn.close()
    return "\n\n".join(schema_parts)

def generate_sql_query(user_query: str, schema: str) -> str:
    """Translate natural language query into valid SQLite SQL using Mistral AI LLM."""
    llm = get_llm_provider()
    
    system_prompt = (
        "You are an expert SQL translator. Your job is to translate a user's natural language question "
        "into a single valid SQLite SQL query based on the database schema provided.\n\n"
        "DATABASE SCHEMA:\n"
        "{schema}\n\n"
        "IMPORTANT RULES:\n"
        "1. Return ONLY the SQLite SQL query code. Do not output any markdown formatting, explanation, or conversational text. "
        "2. Only reference tables and columns defined in the schema.\n"
        "3. Expenses/Withdrawals are represented as NEGATIVE amounts (amount < 0).\n"
        "4. Deposits/Income are represented as POSITIVE amounts (amount > 0).\n"
        "5. If the user asks for 'total spend', 'total expense', or 'spending', select the sum of amounts where amount < 0. Make the sum positive using ABS() if appropriate for display, but sum the negative values.\n"
        "6. If the user asks for 'total income', 'total deposits', or 'earnings', select the sum of amounts where amount > 0.\n"
        "7. The 'date' column is stored as TEXT in 'YYYY-MM-DD' format. To match a month like March 2026, use `date LIKE '2026-03-%'` or `strftime('%m', date) = '03' AND strftime('%Y', date) = '2026'`.\n"
        "8. Perform computations (e.g. SUM, AVG, COUNT, MIN, MAX) directly in SQL; do not fetch raw rows if the question is an aggregate/math question.\n"
        "9. Make description lookups case-insensitive if needed using LIKE, e.g., `description LIKE '%netflix%'.`"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Translate this question into SQLite SQL: {user_query}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    sql_response = chain.invoke({"schema": schema, "user_query": user_query})
    
    # Strip any markdown code blocks returned by LLM
    clean_sql = re.sub(r"```sql|```", "", sql_response).strip()
    return clean_sql

def execute_sql_query(db_path: str, sql_query: str) -> tuple[list[str], list[tuple]]:
    """Execute SQL query on SQLite and return columns and rows."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        return columns, rows
    except Exception as e:
        conn.close()
        raise e
    finally:
        conn.close()

def answer_structured_query(user_query: str) -> dict:
    """
    Orchestrate structured query pipeline:
    NL Query -> Get Schema -> Generate SQL -> Execute SQL -> Format Result dict.
    """
    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(
            f"Database not found at '{DATABASE_PATH}'. "
            "Please run the ingestion pipeline first."
        )
        
    schema = get_sqlite_schema(DATABASE_PATH)
    sql_query = generate_sql_query(user_query, schema)
    
    try:
        columns, rows = execute_sql_query(DATABASE_PATH, sql_query)
        return {
            "query": user_query,
            "sql": sql_query,
            "columns": columns,
            "results": rows,
            "success": True
        }
    except Exception as e:
        return {
            "query": user_query,
            "sql": sql_query,
            "error": str(e),
            "success": False
        }

def main():
    if len(sys.argv) < 2:
        queries = [
            "What was my total spend in March?",
            "What was my TechCorp salary in February 2026?",
            "How much did I spend at Whole Foods in January?",
            "Show total spend grouped by category for January 2026",
            "What is my average transaction amount for Dining?"
        ]
    else:
        queries = [" ".join(sys.argv[1:])]
        
    print("Running Structured SQL Layer Tests...\n")
    for q in queries:
        print(f"Question: '{q}'")
        res = answer_structured_query(q)
        if res["success"]:
            print(f"  Generated SQL: {res['sql']}")
            print(f"  Columns: {res['columns']}")
            print(f"  Rows: {res['results']}")
            # Basic formatting
            if len(res['results']) == 1 and len(res['results'][0]) == 1:
                val = res['results'][0][0]
                if isinstance(val, float):
                    print(f"  Result: ${val:,.2f}")
                else:
                    print(f"  Result: {val}")
            else:
                print("  Result table:")
                for row in res['results']:
                    print(f"    {dict(zip(res['columns'], row))}")
        else:
            print(f"  Generated SQL: {res['sql']}")
            print(f"  Execution Error: {res['error']}")
        print("-" * 60)

if __name__ == "__main__":
    main()
