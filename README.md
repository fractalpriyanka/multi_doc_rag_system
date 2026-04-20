# 📄 PolicyPal MultiDoc RAG

An intelligent **multi-format document understanding and Q&A system** built using **RAG (Retrieval-Augmented Generation)**.

PolicyPal allows users to upload **PDF, DOCX, or Google Docs** and interact with them using a **chat-based interface**, powered by embeddings + vector search + LLM reasoning.

---

# 🚀 Features

* 📥 Multi-format ingestion

  * PDF
  * DOCX
  * Google Docs

* 🧠 Smart structure detection

  * Numeric hierarchy (1, 1.1, 1.1.1)
  * Roman (I, II, III)
  * Alphabetical (A, a)

* 🧩 Intelligent chunking

  * Hierarchy-aware
  * Context-preserving

* 🔍 Semantic search

  * FAISS vector similarity

* 💬 Chat-based UI

  * Streamlit chatbot interface
  * Clean references

* 🔄 Auto-reset system

  * Upload new doc → system resets automatically

---

# 🧠 System Architecture

```
User Input
   ↓
Ingestion (PDF / DOCX / GDoc)
   ↓
Normalization (Hierarchy Detection)
   ↓
Chunking (Context-aware)
   ↓
Embeddings (Sentence Transformers)
   ↓
FAISS Vector Store
   ↓
Query → Retrieval (Top-K)
   ↓
LLM (Groq)
   ↓
Answer + References
```

---

# 📁 Project Structure

```
multi_doc_rag_system/
│
├── app.py                         # Streamlit UI
├── requirements.txt
├── .env
├── .gitignore
│
├── config/
│   └── config.yaml
│
├── ingestion/
│   ├── main_ingestion.py
│   ├── file_loader.py
│   ├── pdf_parser.py
│   ├── docx_parser.py
│   ├── gdoc_parser.py
│   ├── fetch_doc.py
│   ├── normalize.py
│   └── chunker.py
│
├── embedding/
│   ├── embedder.py
│   └── vector_store.py
│
├── retrieval/
│   └── retriever.py
│
├── llm/
│   └── groq_client.py
│
├── temp/                          # temporary uploads
└── __init__.py
```

---

# ⚙️ Installation

## 1️⃣ Clone the repository

```bash
git clone https://github.com/fractalpriyanka/multi_doc_rag_system.git
cd multi_doc_rag_system
```

---

## 2️⃣ Create virtual environment

```bash
python -m venv venv
```

### Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Setup

Create a `.env` file in root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

# ⚙️ Config Setup

Edit `config/config.yaml`:

```yaml
paths:
  raw_data: temp/
  processed_data: temp/
  vector_db: temp/

limits:
  max_file_size_mb: 10

retrieval:
  top_k: 5

model:
  embedding_model: sentence-transformers/all-MiniLM-L6-v2

groq:
  model: llama-3.1-8b-instant
```

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

---

# 💬 How to Use

1. Upload a document OR paste Google Docs link
2. Click **"Process Document"**
3. Ask questions in chat
4. View answers with contextual references
5. Remove document to upload a new one

---

# 🧠 Core Components

## 📥 Ingestion

* Extracts structured text from documents
* Handles:

  * headings
  * tables
  * paragraphs

---

## 🧩 Chunking

* Detects document type:

  * numeric
  * hierarchical
  * mixed
* Creates intelligent chunks preserving context

---

## 🔍 Embedding

* Uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

---

## 📦 Vector Store

* FAISS (in-memory)
* Fast similarity search

---

## 🤖 LLM

* Powered by Groq API
* Context-aware answer generation

---

# 🛠 CLI (Optional Debugging)

You can test ingestion separately:

```bash
python -m ingestion.main_ingestion
```

---

# ⚠️ Limitations

* Single document active at a time
* In-memory vector store (no persistence)
* Large PDFs may take time to process

---

# 🚀 Future Improvements

* Multi-document RAG
* Persistent vector DB (Chroma / Pinecone)
* Reranking models
* Streaming responses
* Frontend (React / Next.js)

---

# 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

# 📜 License

MIT License

---

# 💡 Author

**Priyanka Singh**

AI/ML Enthusiast | Data Scientist | RAG System Builder

---

