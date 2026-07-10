import os
import sys
import sqlite3
import streamlit as st
from gtts import gTTS
import speech_recognition as sr

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

st.markdown("""
<style>
    /* Global Overrides & Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap');
    
    /* Clean custom dark background override */
    .stApp {
        background-color: #0B0F19 !important;
    }
    
    /* Force all standard texts and headers to be light slate */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp li, .stApp div {
        color: #E2E8F0 !important;
    }
    
    /* Heading styling */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #F8FAFC !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Hide Streamlit default decor & headers */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDecoration"] {display: none !important;}
    div[data-testid="stToolbar"] {display: none !important;}
    
    /* Document margins */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    
    /* Typographies */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #38BDF8 0%, #2563EB 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.1rem;
    }
    
    .subtitle {
        font-size: 1rem;
        color: #94A3B8 !important;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Sidebar premium panel */
    section[data-testid="stSidebar"] {
        background-color: #070A13 !important;  /* Dark Slate */
        border-right: 1px solid #1E293B !important;
    }
    
    section[data-testid="stSidebar"] .sidebar-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #F8FAFC !important;
        margin-bottom: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #64748B !important;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 1.5rem;
    }
    
    section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] p {
        color: #94A3B8 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #111827;  /* Dark card background */
        border: 1px solid #1F2937;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.8rem;
    }
    
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #38BDF8 !important;  /* Neon cyan text */
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #94A3B8 !important;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.04em;
    }
    
    /* Custom Quick Queries buttons as SaaS Chips */
    div[data-testid="stButton"] button {
        background-color: #111827 !important;
        color: #E2E8F0 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-testid="stButton"] button:hover {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border-color: #38BDF8 !important;
        transform: translateY(-1px);
    }
    
    /* Chat inputs */
    div[data-testid="stChatInput"] {
        border-radius: 10px !important;
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
    }
    div[data-testid="stChatInput"] textarea {
        color: #F8FAFC !important;
    }
    
    /* Chat bubbles custom styling */
    div[data-testid="stChatMessage"] {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 12px !important;
        padding: 1.1rem !important;
        margin-bottom: 0.9rem !important;
    }
    
    /* Distinguish User message bubble */
    div[data-testid="stChatMessage"][data-testid="chatMessage-user"] {
        background-color: #1F2937 !important;
        border-color: #374151 !important;
    }
    
    /* Pipeline Details styling */
    .pipeline-badge {
        background-color: #111827;
        color: #94A3B8 !important;
        border: 1px solid #1F2937;
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 0.4rem;
    }
    
    .pipeline-badge-sql {
        background-color: #064E3B;
        color: #34D399 !important;
        border-color: #047857;
    }
    
    .pipeline-badge-rag {
        background-color: #3B0764;
        color: #C084FC !important;
        border-color: #6D28D9;
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

# Auto-initialize database and vector index on startup if missing
has_db = os.path.exists(DATABASE_PATH)
has_vs = os.path.exists(VECTOR_STORE_PATH) or os.path.exists(os.path.join(VECTOR_STORE_PATH, "index.faiss"))
if not has_db or not has_vs:
    try:
        from src.ingestion import run_ingestion_pipeline
        run_ingestion_pipeline()
    except Exception as e:
        print(f"Startup ingestion failed: {e}")

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
        
    # Ingestion Uploader Widget
    st.markdown("---")
    st.markdown("### 📥 Ingest New Statement")
    uploaded_file = st.file_uploader("Upload PDF or CSV bank statement", type=["csv", "pdf"])
    if uploaded_file is not None:
        if st.button("Process & Ingest File", use_container_width=True):
            with st.spinner("Parsing and indexing statement..."):
                try:
                    os.makedirs("data", exist_ok=True)
                    save_path = os.path.join("data", uploaded_file.name)
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                        
                    from src.ingestion import run_ingestion_pipeline
                    run_ingestion_pipeline()
                    
                    st.success(f"Successfully ingested {uploaded_file.name}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")
        
    # Voice features setup
    st.markdown("---")
    st.markdown("### 🎙️ Voice Features")
    enable_audio_input = st.checkbox("Enable Audio Input", value=False, help="Record your query through your microphone.")
    enable_audio_output = st.checkbox("Enable Audio Output (TTS)", value=True, help="Synthesize agent responses into spoken text.")

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

# 7. Voice Input Recording (STT)
if enable_audio_input:
    st.markdown("### 🎙️ Voice Input")
    recorded_audio = st.audio_input("Record your question")
    if recorded_audio is not None:
        audio_key = f"audio_{recorded_audio.size}"
        if "last_audio_key" not in st.session_state or st.session_state.last_audio_key != audio_key:
            st.session_state.last_audio_key = audio_key
            audio_bytes = recorded_audio.read()
            
            # Save recorded bytes to scratch directory
            scratch_dir = "C:/Users/Admin/.gemini/antigravity-ide/brain/eb8b816a-3c06-40e5-a12f-4ee742b3923e/scratch"
            os.makedirs(scratch_dir, exist_ok=True)
            temp_audio_path = os.path.join(scratch_dir, "recorded_question.wav")
            with open(temp_audio_path, "wb") as f:
                f.write(audio_bytes)
                
            # Transcribe audio using SpeechRecognition
            r = sr.Recognizer()
            try:
                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = r.record(source)
                transcribed_query = r.recognize_google(audio_data)
                st.session_state.temp_input = transcribed_query
                st.toast(f"🎙️ Transcribed: '{transcribed_query}'")
            except Exception as e:
                st.error(f"Speech transcription failed: {e}")

# 8. Chat History Management
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
            
            # Display TTS audio response if present
            if "audio_path" in p and p["audio_path"] and os.path.exists(p["audio_path"]):
                st.audio(p["audio_path"])
                
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
    # 9. Synthesize Voice Output if enabled
    if enable_audio_output and answer:
        try:
            import time
            # Clean markdown markers for natural speaking flow
            clean_text = answer.replace("**", "").replace("*", "").replace("`", "")
            scratch_dir = "C:/Users/Admin/.gemini/antigravity-ide/brain/eb8b816a-3c06-40e5-a12f-4ee742b3923e/scratch"
            os.makedirs(scratch_dir, exist_ok=True)
            tts_filename = f"response_{int(time.time())}.mp3"
            tts_path = os.path.join(scratch_dir, tts_filename)
            tts = gTTS(text=clean_text, lang="en")
            tts.save(tts_path)
            pipeline_details["audio_path"] = tts_path
        except Exception as e:
            print(f"TTS generation failed: {e}")
            
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(answer)
        
        # Autoplay latest audio response if present
        if "audio_path" in pipeline_details and pipeline_details["audio_path"] and os.path.exists(pipeline_details["audio_path"]):
            st.audio(pipeline_details["audio_path"], autoplay=True)
            
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
