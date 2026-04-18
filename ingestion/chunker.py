import re


# -------------------------------
# 1. DETECT DOCUMENT TYPE
# -------------------------------
def detect_doc_type(sections):

    numeric = 0
    roman = 0
    alpha = 0

    for sec in sections[:50]:

        sid = sec.get("section_id", "")

        if re.match(r"^\d+(\.\d+)*$", sid):
            numeric += 1

        elif re.match(r"^[IVX]+", sid):
            roman += 1

        elif re.match(r"^[A-Za-z]", sid):
            alpha += 1

    if numeric > max(roman, alpha):
        return "numeric"

    elif roman > max(numeric, alpha):
        return "hierarchical"

    else:
        return "mixed"


# -------------------------------
# 2. CLEAN TEXT
# -------------------------------
def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -------------------------------
# 3. SPLIT LONG TEXT
# -------------------------------
def split_text(text, max_words=120):

    words = text.split()

    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks


# -------------------------------
# 4. HIERARCHY PATH BUILDER
# -------------------------------
def build_hierarchy_path(section_id):

    return section_id.split(".")


# -------------------------------
# 5. MAIN CHUNKING FUNCTION
# -------------------------------
def chunk_sections(data):

    sections = data.get("sections", [])

    doc_type = detect_doc_type(sections)

    chunks = []

    for sec in sections:

        section_id = sec.get("section_id", "")
        title = sec.get("title", "")
        text = clean_text(sec.get("text", ""))

        if not text:
            continue

        # 🔹 Strategy 1: Numeric (PDF type)
        if doc_type == "numeric":

            split_chunks = split_text(text, 120)

            for i, chunk_text in enumerate(split_chunks):

                chunks.append({
                    "chunk_id": f"{section_id}_{i}",
                    "section_id": section_id,
                    "title": title,
                    "text": chunk_text,
                    "path": build_hierarchy_path(section_id)
                })

        # 🔹 Strategy 2: Hierarchical (handbook type)
        elif doc_type == "hierarchical":

            chunks.append({
                "chunk_id": section_id,
                "section_id": section_id,
                "title": title,
                "text": text,
                "path": build_hierarchy_path(section_id)
            })

        # 🔹 Strategy 3: Mixed (ESG / hybrid)
        else:

            split_chunks = split_text(text, 100)

            for i, chunk_text in enumerate(split_chunks):

                chunks.append({
                    "chunk_id": f"{section_id}_{i}",
                    "section_id": section_id,
                    "title": title,
                    "text": chunk_text,
                    "path": build_hierarchy_path(section_id)
                })

    return {
        "doc_type": doc_type,
        "total_chunks": len(chunks),
        "chunks": chunks
    }