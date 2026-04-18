from groq import Groq
import os
from dotenv import load_dotenv

# 🔥 FORCE LOAD ENV
load_dotenv()

def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(context_chunks, query, config):

    client = get_groq_client()

    # Build context
    context_text = "\n\n".join([
        f"[{c['section_id']}] {c['title']}: {c['text']}"
        for c in context_chunks
    ])

    prompt = f"""
You are a strict policy assistant.

IMPORTANT RULES:
1. Answer ONLY using the provided context.
2. Do NOT use prior knowledge.
3. If answer is not found in context, say:
   "I cannot find this information in the provided document."
4. Do NOT guess or hallucinate.


CONTEXT:
{context_text}

QUESTION:
{query}

OUTPUT FORMAT:
- Answer:
- Supporting Sections: [section_id]
- Confidence: High / Medium / Low

Now answer:
"""

    response = client.chat.completions.create(
        model=config["groq"]["model"],
        temperature=0,  # 🔥 critical to reduce hallucination
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content