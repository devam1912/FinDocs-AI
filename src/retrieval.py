import os
import sys
from langchain_community.vectorstores import FAISS
from langchain_mistralai import MistralAIEmbeddings

try:
    from src.config import MISTRAL_API_KEY, VECTOR_STORE_PATH
except ImportError:
    # Handle direct script executions
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.config import MISTRAL_API_KEY, VECTOR_STORE_PATH

def load_vectorstore(vectorstore_path: str, api_key: str) -> FAISS:
    """Load the local FAISS vector store index."""
    if not os.path.exists(vectorstore_path) and not os.path.exists(f"{vectorstore_path}.faiss"):
        # Look for index files in the target directory
        if not os.path.isdir(vectorstore_path) or not os.path.exists(os.path.join(vectorstore_path, "index.faiss")):
            raise FileNotFoundError(
                f"FAISS index not found at '{vectorstore_path}'. "
                "Please run the ingestion pipeline first."
            )
            
    embeddings = MistralAIEmbeddings(
        mistral_api_key=api_key,
        model="mistral-embed"
    )
    # allow_dangerous_deserialization is required to load local FAISS pickle files
    return FAISS.load_local(vectorstore_path, embeddings, allow_dangerous_deserialization=True)

def retrieve_documents(query: str, k: int = 5) -> list:
    """Retrieve top-k relevant transaction chunks matching the query."""
    vectorstore = load_vectorstore(VECTOR_STORE_PATH, MISTRAL_API_KEY)
    return vectorstore.similarity_search(query, k=k)

def main():
    if len(sys.argv) < 2:
        # Default testing queries
        queries = [
            "Netflix subscription cost",
            "How much was spent at Apple Store?",
            "Transactions in Whole Foods Market",
            "Freelance Client deposits"
        ]
    else:
        queries = [" ".join(sys.argv[1:])]
        
    print("Running Manual Retrieval Layer Tests...\n")
    for q in queries:
        print(f"Query: '{q}'")
        try:
            results = retrieve_documents(q, k=3)
            print(f"Retrieved {len(results)} matches:")
            for idx, doc in enumerate(results):
                print(f"  Match {idx+1}:")
                print(f"    Content: {doc.page_content}")
                print(f"    Metadata: {doc.metadata}")
            print("-" * 50)
        except Exception as e:
            print(f"  Error performing retrieval: {e}")
            print("-" * 50)

if __name__ == "__main__":
    main()
