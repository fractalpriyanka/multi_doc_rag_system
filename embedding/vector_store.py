import faiss
import numpy as np
import os
import pickle


def create_faiss_index(embeddings):

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)  # cosine similarity (since normalized)

    index.add(embeddings)

    return index


def save_index(index, metadata, path="vector_db"):

    os.makedirs(path, exist_ok=True)

    faiss.write_index(index, os.path.join(path, "index.faiss"))

    with open(os.path.join(path, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Vector DB saved")


def load_index(path="vector_db"):

    index = faiss.read_index(os.path.join(path, "index.faiss"))

    with open(os.path.join(path, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search(index, query_embedding, top_k=5):

    scores, indices = index.search(query_embedding, top_k)

    return scores, indices