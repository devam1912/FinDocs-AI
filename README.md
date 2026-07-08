# FinDocs AI

A RAG + Agent + Evals system for querying financial documents (bank statements, expense reports) using LangChain, Mistral AI, and Streamlit.

## Tech Stack
- **Core**: Python
- **LLM/Agent Framework**: LangChain + Mistral AI API
- **Vector Database**: FAISS or Chroma
- **Structured Database**: SQLite
- **Evaluation**: pytest
- **Frontend**: Streamlit

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/devam1912/FinDocs-AI.git
   cd FinDocs-AI
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - Copy `.env.example` to `.env` and fill in your `MISTRAL_API_KEY`.
   - Local secrets for Streamlit can also be configured in `.streamlit/secrets.toml`.

## Repository Structure

- `data/`: Raw bank statements and expense reports (PDF/CSV).
- `db/`: SQLite database storage.
- `vectorstore/`: Local FAISS or Chroma vector indexes.
- `src/`: Core Python modules for config, ingestion, retrieval, agent, and logging/observation.
- `tests/`: Evaluation harness and test scripts.
- `ui/`: Streamlit web interface.

## Running the Project

- **Generate Mock Data**: (To be implemented)
- **Run Ingestion**: (To be implemented)
- **Run Streamlit UI**:
  ```bash
  streamlit run ui/app.py
  ```
- **Run Evaluations**:
  ```bash
  pytest tests/
  ```

## Live Demo
*Link to Streamlit Community Cloud deployment will be placed here.*
