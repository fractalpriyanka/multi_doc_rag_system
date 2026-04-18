from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import yaml

from ingestion.main_ingestion import ingest_input
from retrieval.retriever import retrieve
from llm.groq_client import generate_answer


# -------------------------------
# LOAD CONFIG
# -------------------------------
def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "config.yaml")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)


config = load_config()

os.makedirs("/tmp/data", exist_ok=True)
os.makedirs("/tmp/vector_db", exist_ok=True)

# -------------------------------
# INIT APP
# -------------------------------
app = FastAPI(title="PolicyPal Backend")


# Allow frontend later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs(config["paths"]["vector_db"], exist_ok=True)


# -------------------------------
# 1. INGEST ENDPOINT
# -------------------------------
@app.post("/ingest")
async def ingest(
    input_type: str = Form(...),
    file: UploadFile = File(None),
    link: str = Form(None)
):

    try:

        # 🔹 FILE INPUT
        if input_type == "file":

            if file is None:
                return {"error": "No file uploaded"}

            file_path = os.path.join("data", file.filename)

            with open(file_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            result = ingest_input("file", file_path)

        # 🔹 LINK INPUT
        elif input_type == "link":

            if not link:
                return {"error": "No link provided"}

            result = ingest_input("link", link)

        else:
            return {"error": "Invalid input type"}

        return {
            "status": "success",
            "message": "Document processed",
            "total_chunks": result["total_chunks"]
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 2. QUERY ENDPOINT
# -------------------------------
@app.post("/query")
async def query_api(question: str = Form(...)):

    try:

        chunks = retrieve(question, config)

        answer = generate_answer(chunks, question, config)

        return {
            "answer": answer,
            "sources": chunks
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 3. RESET (DELETE VECTOR DB)
# -------------------------------
@app.delete("/reset")
async def reset():

    try:
        vector_path = config["paths"]["vector_db"]

        if os.path.exists(vector_path):
            shutil.rmtree(vector_path)

        os.makedirs(vector_path, exist_ok=True)

        return {"status": "success", "message": "Vector DB cleared"}

    except Exception as e:
        return {"error": str(e)}


# -------------------------------
# 4. HEALTH CHECK
# -------------------------------
@app.get("/")
def root():
    return {"message": "PolicyPal Backend Running 🚀"}
