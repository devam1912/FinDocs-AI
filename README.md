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
- `vectorstore/`: Local FAISS vector index.
- `logs/`: Local agent interaction logs (ignored by git).
- `src/`: Core Python modules for config, ingestion, retrieval, structured querying, agent, and logging/observation.
- `scripts/`: Data generation and evals harness scripts.
- `tests/`: Unit test suite.
- `ui/`: Streamlit web interface.

## Running the Project

1. **Generate Mock Data**:
   ```bash
   python scripts/generate_mock_data.py
   ```

2. **Run Ingestion Pipeline**:
   ```bash
   python src/ingestion.py
   ```

3. **Run Streamlit Dashboard UI (includes Voice support)**:
   ```bash
   streamlit run ui/app.py
   ```

4. **Run Evaluations Harness**:
   ```bash
   python scripts/run_evals.py
   ```

5. **Run Pytest Suite**:
   ```bash
   pytest tests/
   ```

## 🚀 Streamlit Cloud Deployment

To deploy this application to Streamlit Community Cloud (free tier):

1. Commit and push all changes to your GitHub repository: `https://github.com/devam1912/FinDocs-AI`.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app**, select your repository (`devam1912/FinDocs-AI`), branch (`main`), and set the main file path to `ui/app.py`.
4. Before deploying, click **Advanced settings...** and paste your API keys under **Secrets**:
   ```toml
   MISTRAL_API_KEY = "your-mistral-api-key-here"
   ```
5. Click **Deploy**. Your app will be live in a couple of minutes!

## 🔗 Live Demo
* [FinDocs AI Live Deployment](https://findocs-ai.streamlit.app) *(Note: User to replace this with their actual deployed Streamlit Community Cloud URL)*
