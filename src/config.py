import os
from dotenv import load_dotenv

# Load environment variables from .env file for local command-line runs
load_dotenv()

# Strategy Pattern Configuration or standard environment variable lookup
def get_config(key: str, default: str = "") -> str:
    """
    Retrieve configuration value, prioritizing Streamlit secrets if available,
    otherwise falling back to environment variables.
    """
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except ImportError:
        pass
    
    return os.getenv(key, default)

LLM_PROVIDER = get_config("LLM_PROVIDER", "mistral")
MISTRAL_API_KEY = get_config("MISTRAL_API_KEY", "")
DATABASE_PATH = get_config("DATABASE_PATH", "db/findocs.db")
VECTOR_STORE_PATH = get_config("VECTOR_STORE_PATH", "vectorstore/faiss_index")
