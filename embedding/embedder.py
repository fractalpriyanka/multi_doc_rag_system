from sentence_transformers import SentenceTransformer

model = None

def load_model(model_name):
    global model
    if model is None:
        model = SentenceTransformer(model_name)
    return model


def embed_texts(texts, config):
    model = load_model(config["model"]["embedding_model"])
    return model.encode(texts, show_progress_bar=True)