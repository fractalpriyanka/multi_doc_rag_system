import faiss
import numpy as np

VECTOR_STORE = {
    "index": None,
    "metadata": []
}


def create_index(embeddings, metadata):

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    VECTOR_STORE["index"] = index
    VECTOR_STORE["metadata"] = metadata


def search(query_embedding, top_k=5):

    index = VECTOR_STORE["index"]

    if index is None:
        return []

    D, I = index.search(query_embedding, top_k)

    results = []
    for idx in I[0]:
        results.append(VECTOR_STORE["metadata"][idx])

    return results


def reset_store():
    VECTOR_STORE["index"] = None
    VECTOR_STORE["metadata"] = []