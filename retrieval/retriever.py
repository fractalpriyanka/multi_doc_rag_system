from embedding.embedder import model
from embedding.vector_store import load_index, search
import numpy as np


def retrieve(query, config):

    index, metadata = load_index(config["paths"]["vector_db"])

    # 🔥 embed query
    query_embedding = model.encode([query], normalize_embeddings=True)

    scores, indices = search(index, query_embedding, config["retrieval"]["top_k"])

    results = []

    for idx in indices[0]:
        results.append(metadata[idx])

    return results