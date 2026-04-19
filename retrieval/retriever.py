from embedding.embedder import embed_texts
from embedding.vector_store import search


def retrieve(query, config):

    query_embedding = embed_texts([query], config)

    results = search(query_embedding, config["retrieval"]["top_k"])

    return results