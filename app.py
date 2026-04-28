import streamlit as st
import yaml
import os

from ingestion.main_ingestion import ingest_input
from ingestion.chunker import chunk_sections

from embedding.embedder import embed_texts
from embedding.vector_store import create_index, reset_store

from retrieval.retriever import retrieve
from llm.groq_client import generate_answer


# ---------- CONFIG ----------
def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


config = load_config()


# ---------- PAGE ----------
st.set_page_config(
    page_title="PolicyPal · MultiDoc RAG",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #13131c;
    --surface2:  #1c1c2a;
    --border:    #2a2a3d;
    --accent:    #c8ff57;
    --accent2:   #7b61ff;
    --text:      #e8e8f0;
    --muted:     #6b6b85;
    --user-bg:   #1e1e30;
    --bot-bg:    #161624;
    --radius:    14px;
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="collapsedControl"] { opacity:0.35; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.5rem !important; }

.sidebar-logo {
    font-family: var(--font-head);
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.sidebar-tagline {
    font-size: 0.74rem;
    color: var(--muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
.section-label {
    font-family: var(--font-head);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.4rem 0 0.6rem;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 1.4rem 0;
}

/* ── Source type toggle buttons ── */
[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--muted) !important;
    font-family: var(--font-head) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    padding: 0.4rem 0.6rem !important;
}
[data-testid="stSidebar"] button:hover {
    border-color: var(--accent2) !important;
    color: var(--text) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stFileUploader"] label { color: var(--muted) !important; font-size: 0.82rem !important; }
[data-testid="stFileUploaderDeleteBtn"] { display: none !important; }

/* ── Text input ── */
[data-testid="stTextInput"] input {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 0.9rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(123,97,255,0.15) !important;
}
[data-testid="stTextInput"] label { color: var(--muted) !important; font-size: 0.78rem !important; }

/* ── Source badge ── */
.source-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.55rem 0.85rem;
    font-size: 0.8rem;
    color: var(--text);
    margin-bottom: 0.75rem;
}
.badge-icon { font-size: 1rem; }
.badge-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.badge-type {
    font-size: 0.65rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--accent);
    font-weight: 700;
    font-family: var(--font-head);
}

/* ── Info / warning alerts ── */
[data-testid="stAlert"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--muted) !important;
    font-size: 0.8rem !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label { color: var(--muted) !important; font-size: 0.84rem !important; }
[data-testid="stRadio"] { background: transparent !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: var(--muted) !important; font-size: 0.82rem !important; }

/* ── Main header ── */
.chat-header {
    text-align: center;
    padding: 2.2rem 0 1.2rem;
}
.chat-header h1 {
    font-family: var(--font-head);
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin: 0;
}
.chat-header h1 span { color: var(--accent); }
.chat-header p {
    color: var(--muted);
    font-size: 0.88rem;
    margin-top: 0.45rem;
    font-weight: 300;
}

/* ── Active source bar ── */
.active-source-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(200,255,87,0.06);
    border: 1px solid rgba(200,255,87,0.2);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    color: var(--accent);
    font-family: var(--font-head);
    font-weight: 600;
    margin-bottom: 1rem;
}
.active-source-bar span { color: var(--muted); font-weight: 400; font-family: var(--font-body); }

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--muted);
}
.empty-icon { font-size: 3.5rem; margin-bottom: 1rem; opacity: 0.4; }
.empty-state h3 {
    font-family: var(--font-head);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--muted);
    margin-bottom: 0.3rem;
}
.empty-state p { font-size: 0.82rem; line-height: 1.6; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--bot-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.1rem !important;
    margin-bottom: 0.8rem !important;
    animation: fadeUp 0.25s ease both;
}
[data-testid="stChatMessage"][data-testid*="user"] {
    background: var(--user-bg) !important;
    border-color: rgba(200,255,87,0.12) !important;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"] p {
    color: var(--text) !important;
    font-size: 0.88rem !important;
    line-height: 1.65 !important;
    font-family: var(--font-body) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(123,97,255,0.12) !important;
}

/* ── References expander ── */
[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-top: 0.8rem !important;
}
[data-testid="stExpander"] summary {
    font-family: var(--font-head) !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: var(--muted) !important;
    letter-spacing: 0.03em !important;
    padding: 0.65rem 1rem !important;
}
[data-testid="stExpander"] summary:hover { color: var(--text) !important; }
[data-testid="stExpander"] svg { fill: var(--muted) !important; }
[data-testid="stExpanderDetails"] {
    border-top: 1px solid var(--border) !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMarkdown"] h3 {
    font-family: var(--font-head) !important;
    font-size: 0.9rem !important;
    color: var(--accent2) !important;
    font-weight: 700 !important;
}
[data-testid="stDivider"] { border-color: var(--border) !important; opacity: 0.5 !important; }

/* ── Success / warning ── */
[data-testid="stSuccess"] {
    background: rgba(200,255,87,0.07) !important;
    border: 1px solid rgba(200,255,87,0.25) !important;
    border-radius: var(--radius) !important;
    color: var(--accent) !important;
    font-size: 0.82rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "processed" not in st.session_state:
    st.session_state.processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "doc_loaded" not in st.session_state:
    st.session_state.doc_loaded = False


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✦ PolicyPal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">MultiDoc RAG Assistant</div>', unsafe_allow_html=True)

    # ── Upload section ──
    st.markdown('<div class="section-label">Knowledge Source</div>', unsafe_allow_html=True)
    st.info("⚠️ File size should not exceed 10 MB")

    input_type = st.radio(
        "Select Input Type",
        ["File", "Google Doc Link"],
        label_visibility="collapsed",
    )

    file = None
    link = None

    if input_type == "File":
        st.markdown('<div class="section-label">Upload Document</div>', unsafe_allow_html=True)
        file = st.file_uploader(
            "Upload PDF / DOCX",
            type=["pdf", "docx"],
            label_visibility="collapsed",
        )
        # Show badge for loaded file (native remove btn is hidden via CSS)
        if file and st.session_state.doc_loaded:
            short = file.name[:28] + "…" if len(file.name) > 28 else file.name
            st.markdown(f"""
            <div class="source-badge">
                <span class="badge-icon">📄</span>
                <span class="badge-name">{short}</span>
                <span class="badge-type">DOC</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-label">Paste a Link</div>', unsafe_allow_html=True)
        link = st.text_input(
            "Google Docs link",
            placeholder="https://docs.google.com/...",
            label_visibility="collapsed",
        )
        if link and st.session_state.doc_loaded:
            short = link[:28] + "…" if len(link) > 28 else link
            st.markdown(f"""
            <div class="source-badge">
                <span class="badge-icon">🔗</span>
                <span class="badge-name">{short}</span>
                <span class="badge-type">URL</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── Auto-process as soon as a file/link is provided ──
    if not st.session_state.doc_loaded:
        if (input_type == "File" and file) or \
           (input_type == "Google Doc Link" and link and link.strip()):
            with st.spinner("Reading your document…"):
                if input_type == "File" and file:
                    file_path = os.path.join("temp", file.name)
                    os.makedirs("temp", exist_ok=True)
                    with open(file_path, "wb") as f:
                        f.write(file.read())
                    data = ingest_input("file", file_path)
                else:
                    data = ingest_input("link", link)

                chunked_data = chunk_sections(data)
                chunks = chunked_data["chunks"]

                texts = [
                    f"{c['section_id']} {c['title']} {c['text']}"
                    for c in chunks
                ]

                embeddings = embed_texts(texts, config)
                create_index(embeddings, chunks)

                st.session_state.processed = True
                st.session_state.doc_loaded = True
                st.session_state.chat_history = []

            st.success("✅ All set! Go ahead and ask anything.")

    # ── Remove document ──
    if st.session_state.doc_loaded:
        if st.button("🗑️  Remove Document", use_container_width=True):
            reset_store()
            st.session_state.processed = False
            st.session_state.doc_loaded = False
            st.session_state.chat_history = []
            st.success("Document removed. Upload a new one.")

    # ── Session stats ──
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    n = len(st.session_state.chat_history)
    st.markdown(f"""
    <div style="font-size:0.75rem;color:var(--muted);line-height:2.2;">
        💬 &nbsp;<b style="color:var(--text)">{n // 2}</b> exchanges<br>
        🗂 &nbsp;<b style="color:var(--text)">{'1 source active' if st.session_state.doc_loaded else 'No source loaded'}</b>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN AREA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
  <h1>Ask <span>PolicyPal</span></h1>
  <p>Upload a document or paste a Google Doc link — then start your conversation.</p>
</div>
""", unsafe_allow_html=True)

# Active source indicator
if st.session_state.doc_loaded:
    icon  = "📄" if input_type == "File" else "🔗"
    name  = (file.name if file else link) or "source"
    short = name[:60] + "…" if len(name) > 60 else name
    st.markdown(f"""
    <div class="active-source-bar">
        {icon} &nbsp;Ready to chat &nbsp;
        <span>— {short}</span>
    </div>
    """, unsafe_allow_html=True)

# ── Chat UI ──
if st.session_state.processed:

    user_query = st.chat_input("Ask something about the document...")

    if user_query:
        st.session_state.chat_history.append(("user", user_query))

        with st.spinner("Thinking..."):
            results = retrieve(user_query, config)
            answer = generate_answer(results, user_query, config)

        st.session_state.chat_history.append(("bot", answer))

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.write(msg)
        else:
            with st.chat_message("assistant"):
                st.write(msg)

    # References — collapsed by default inside an expander
    if st.session_state.chat_history:
        results = retrieve(st.session_state.chat_history[-2][1], config)
        with st.expander("📚 Where did this answer come from?", expanded=False):
            for c in results:
                st.markdown(f"**{c['title']}**")
                st.write(c["text"])
                st.divider()

else:
    # Empty state when no doc processed yet
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">✦</div>
        <h3>No document loaded yet</h3>
        <p>Upload a PDF / DOCX or paste a Google Doc link<br>from the sidebar, then hit <b>Process Document</b>.</p>
    </div>
    """, unsafe_allow_html=True)
