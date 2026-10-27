from google import genai
import os
from dotenv import load_dotenv

load_dotenv()


def get_groq_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    return genai.Client(api_key=api_key)


def generate_answer(context_chunks, query, config):

    client = get_groq_client()

    context_text = "\n\n".join([
        f"{c['section_id']} {c['title']}: {c['text']}"
        for c in context_chunks
    ])

    prompt = f"""
You are a policy assistant.

Use ONLY the given context.
If answer not found, say "Not found in document".

Context:
{context_text}

Question:
{query}
"""

    response = client.models.generate_content(
        model=config["groq"]["model"],
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text

