import yaml

from ingestion.file_loader import detect_file_type
from ingestion.pdf_parser import parse_pdf
from ingestion.docx_parser import parse_docx
from ingestion.gdoc_parser import process_google_doc
from ingestion.chunker import chunk_sections

from embedding.embedder import embed_chunks
from embedding.vector_store import create_faiss_index, save_index


def load_config():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def ingest_input(input_type, input_value):

    config = load_config()
    raw_path = config["paths"]["raw_data"]

    parsed_data = None

    # 🔹 LINK
    if input_type == "link":

        if "docs.google.com" not in input_value:
            raise ValueError("Only Google Docs links supported")

        parsed_data = process_google_doc(input_value, raw_path)

    # 🔹 FILE
    elif input_type == "file":

        file_type = detect_file_type(input_value)

        if file_type == "pdf":
            parsed_data = parse_pdf(input_value)

        elif file_type == "docx":
            parsed_data = parse_docx(input_value)

        else:
            raise ValueError("Unsupported file type")

    else:
        raise ValueError("Invalid input type")

    # 🔥 CHUNKING
    chunked_data = chunk_sections(parsed_data)

    chunks = chunked_data["chunks"]

    # 🔥 EMBEDDING
    embeddings, texts = embed_chunks(chunks)

    # 🔥 VECTOR DB
    index = create_faiss_index(embeddings)

    # store metadata (chunks)
    save_index(index, chunks)

    return {
        "status": "success",
        "total_chunks": len(chunks)
    }