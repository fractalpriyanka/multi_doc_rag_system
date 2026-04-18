from sentence_transformers import SentenceTransformer


# 🔥 Load model once
model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def create_embedding_text(chunk):
    """
    Combine hierarchy + title + text
    THIS IS VERY IMPORTANT FOR POLICY DOCS
    """

    section_id = chunk.get("section_id", "")
    title = chunk.get("title", "")
    text = chunk.get("text", "")

    return f"{section_id} {title}. {text}"


def embed_chunks(chunks):

    texts = [create_embedding_text(c) for c in chunks]

    embeddings = model.encode(texts, normalize_embeddings=True)

    return embeddings, texts