import os
import sys
import sqlite3
import streamlit as st

# Setup python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.agent import run_agent
    from src.config import DATABASE_PATH, VECTOR_STORE_PATH
except ImportError:
    # Fallback paths
    from src.agent import run_agent
    from src.config import DATABASE_PATH, VECTOR_STORE_PATH

# 1. Page Configuration
st.set_page_config(
    page_title="FinDocs AI - RAG & SQL Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium CSS Custom Styling Injection
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #4A5568;
        margin-bottom: 2rem;
    }
    
    /* Card Styles */
    .metric-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1A365D;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #718096;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    /* Chat Customizations */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px 0 rgba(0,0,0,0.02);
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #1A365D;
        margin-bottom: 1.5rem;
    }
    
    /* Pipeline Details styling */
    .pipeline-badge {
        background-color: #EBF8FF;
        color: #2B6CB0;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    .pipeline-badge-sql {
        background-color: #F0FFF4;
        color: #2F855A;
    }
    
    .pipeline-badge-rag {
        background-color: #FAF5FF;
        color: #6B46C1;
    }
</style>
""", unsafe_allow_html=True)

# 3. Database Info Fetching Helpers
def get_db_stats():
    """Retrieve statistics from the SQLite database."""
    stats = {"total_tx": 0, "categories": 0, "statements": []}
    if not os.path.exists(DATABASE_PATH):
        return stats
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Get total transaction count
        cursor.execute("SELECT COUNT(*) FROM transactions;")
        stats["total_tx"] = cursor.fetchone()[0]
        
        # Get distinct categories
        cursor.execute("SELECT COUNT(DISTINCT category) FROM transactions;")
        stats["categories"] = cursor.fetchone()[0]
        
        # Get distinct files ingested
        cursor.execute("SELECT DISTINCT source_file FROM transactions;")
        stats["statements"] = [r[0] for r in cursor.fetchall()]
        
        conn.close()
    except Exception as e:
        print(f"Error loading stats from SQLite: {e}")
    return stats

db_stats = get_db_stats()

# 4. Sidebar Layout
with st.sidebar:
    st.markdown('<div class="sidebar-header">💼 FinDocs AI Panel</div>', unsafe_allow_html=True)
    st.markdown("### 📊 Ingestion Status")
    
    # Render Stats Cards
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{db_stats['total_tx']}</div>
        <div class="metric-label">Total Transactions Ingested</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{db_stats['categories']}</div>
        <div class="metric-label">Active Spending Categories</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Vector store index status
    has_vs = os.path.exists(VECTOR_STORE_PATH) or os.path.exists(f"{VECTOR_STORE_PATH}.faiss")
    st.markdown("### 🗄️ Vector Store Status")
    if has_vs:
        st.success("FAISS Index: Active")
    else:
        st.error("FAISS Index: Missing")
        
    # Statements files list
    st.markdown("### 📂 Ingested Statements")
    if db_stats["statements"]:
        for f in db_stats["statements"]:
            st.caption(f"📄 {f}")
    else:
        st.caption("No statements ingested yet.")

# 5. Main Dashboard Header
st.markdown('<div class="main-title">💼 FinDocs AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Agentic financial document reasoning combining semantic vector search and direct SQLite execution.</div>', unsafe_allow_html=True)

# 6. Sample Template Questions
st.markdown("### 💡 Quick Queries")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Spend in March?", use_container_width=True):
        st.session_state.temp_input = "What was my total spend in March?"
with col2:
    if st.button("🎵 Spotify Payments?", use_container_width=True):
        st.session_state.temp_input = "find my transaction for Spotify Premium"
with col3:
    if st.button("🍔 Category Grouping?", use_container_width=True):
        st.session_state.temp_input = "Show total spend grouped by category for January 2026"
with col4:
    if st.button("💵 TechCorp Payout?", use_container_width=True):
        st.session_state.temp_input = "What was my TechCorp salary in February 2026?"

# 7. Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display dialogue history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Display pipeline details if present (for assistant messages)
        if msg["role"] == "assistant" and "pipeline" in msg:
            p = msg["pipeline"]
            
            # Setup intent badges
            badge_class = "pipeline-badge-sql" if p["intent"] == "STRUCTURED_SQL" else "pipeline-badge-rag"
            st.markdown(
                f'<span class="pipeline-badge {badge_class}">Intent: {p["intent"]}</span>'
                f'<span class="pipeline-badge">Tool: {p["tool"]}</span>'
                f'<span class="pipeline-badge">Time: {p["latency"]:.3f}s</span>',
                unsafe_allow_html=True
            )
            
            # Tool-specific details expander
            with st.expander("🛠️ Query Execution Details"):
                if p["intent"] == "STRUCTURED_SQL" and p["tool_result"]:
                    tr = p["tool_result"]
                    if "sql_query" in tr:
                        st.markdown("**Executed SQL Query:**")
                        st.code(tr["sql_query"], language="sql")
                    if "data" in tr:
                        st.markdown("**Database Outputs:**")
                        st.dataframe(tr["data"])
                        
                elif p["intent"] == "RETRIEVAL" and p["tool_result"]:
                    tr = p["tool_result"]
                    if "documents" in tr:
                        st.markdown("**Retrieved semantic chunks:**")
                        for idx, doc in enumerate(tr["documents"]):
                            st.info(f"**Chunk {idx+1} (Source: {doc['metadata'].get('source')}):**\n{doc['content']}")

# 8. Chat Input Handling
# Allow clicking template buttons to pre-populate input
user_query = st.chat_input("Ask a question about your bank statements...")

if "temp_input" in st.session_state and st.session_state.temp_input:
    user_query = st.session_state.temp_input
    st.session_state.temp_input = None

if user_query:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Process with Agent RAG/SQL CoR Pipeline
    with st.spinner("Agent routing and reasoning..."):
        try:
            ctx = run_agent(user_query)
            
            if ctx.success:
                answer = ctx.final_response
                pipeline_details = {
                    "intent": ctx.intent,
                    "tool": ctx.tool_to_use,
                    "latency": ctx.metadata.get("total_latency", 0.0),
                    "tool_result": ctx.tool_result
                }
            else:
                answer = f"⚠️ Pipeline error: {ctx.error}"
                pipeline_details = {
                    "intent": ctx.intent or "UNKNOWN",
                    "tool": ctx.tool_to_use or "NONE",
                    "latency": ctx.metadata.get("total_latency", 0.0),
                    "tool_result": None
                }
        except Exception as e:
            answer = f"⚠️ Exception occurred during reasoning: {str(e)}"
            pipeline_details = {
                "intent": "ERROR",
                "tool": "NONE",
                "latency": 0.0,
                "tool_result": None
            }
            
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
        
        # Setup intent badges
        badge_class = "pipeline-badge-sql" if pipeline_details["intent"] == "STRUCTURED_SQL" else "pipeline-badge-rag"
        st.markdown(
            f'<span class="pipeline-badge {badge_class}">Intent: {pipeline_details["intent"]}</span>'
            f'<span class="pipeline-badge">Tool: {pipeline_details["tool"]}</span>'
            f'<span class="pipeline-badge">Time: {pipeline_details["latency"]:.3f}s</span>',
            unsafe_allow_html=True
        )
        
        # Details expander
        with st.expander("🛠️ Query Execution Details"):
            if pipeline_details["intent"] == "STRUCTURED_SQL" and pipeline_details["tool_result"]:
                tr = pipeline_details["tool_result"]
                if "sql_query" in tr:
                    st.markdown("**Executed SQL Query:**")
                    st.code(tr["sql_query"], language="sql")
                if "data" in tr:
                    st.markdown("**Database Outputs:**")
                    st.dataframe(tr["data"])
            elif pipeline_details["intent"] == "RETRIEVAL" and pipeline_details["tool_result"]:
                tr = pipeline_details["tool_result"]
                if "documents" in tr:
                    st.markdown("**Retrieved semantic chunks:**")
                    for idx, doc in enumerate(tr["documents"]):
                        st.info(f"**Chunk {idx+1} (Source: {doc['metadata'].get('source')}):**\n{doc['content']}")
                        
    # Append to dialogue state
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "pipeline": pipeline_details
    })
    
    # Force state refresh
    st.rerun()
