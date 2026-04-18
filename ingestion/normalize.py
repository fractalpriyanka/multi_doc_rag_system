import re


def normalize_text(text):
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_heading(text):

    if not text:
        return False

    words = text.split()

    # Avoid long sentences
    if len(words) > 12:
        return False

    # Avoid table rows
    if len(words) <= 2 and text.isupper():
        return False

    if re.search(r"[&/]", text):
        return False

    # Roman
    if re.match(r"^[IVX]+\.?\s+", text):
        return True

    # Numeric (supports 5.1, 5.1.2)
    if re.match(r"^\d+(\.\d+)*\.?\s+", text):
        return True

    # Alphabet
    if re.match(r"^[A-Z]\.\s+", text):
        return True

    if re.match(r"^[a-z]\.\s+", text):
        return True

    # CAPS headings
    if text.isupper() and len(words) > 2:
        return True

    return False


def extract_prefix(text):
    match = re.match(r"^([IVX]+|\d+(\.\d+)*|[A-Za-z])\.?\s+(.*)", text)
    if match:
        return match.group(1), match.group(3)
    return "", text


def is_toc_line(text):
    return bool(re.search(r"\.{3,}", text)) or bool(re.search(r"\d+$", text))


def update_hierarchy(h, prefix):

    # Numeric hierarchy (5, 5.1, 5.1.2)
    if re.match(r"^\d+(\.\d+)*$", prefix):
        h["num"] = prefix
        h["roman"] = ""
        h["alpha_upper"] = ""
        h["alpha_lower"] = ""

    # Roman
    elif re.match(r"^[IVX]+$", prefix):
        h["roman"] = prefix
        h["num"] = ""
        h["alpha_upper"] = ""
        h["alpha_lower"] = ""

    # Upper alpha
    elif len(prefix) == 1 and prefix.isupper():
        h["alpha_upper"] = prefix
        h["alpha_lower"] = ""

    # Lower alpha
    elif len(prefix) == 1 and prefix.islower():
        h["alpha_lower"] = prefix

    return h


def build_section_id(h):

    import re

    # 🔹 Case 1: multi-level numeric (5.1, 5.1.2)
    if h.get("num") and re.match(r"^\d+\.\d+", h["num"]):
        return h["num"]

    parts = []

    if h.get("roman"):
        parts.append(h["roman"])

    if h.get("alpha_upper"):
        parts.append(h["alpha_upper"])

    if h.get("num"):
        parts.append(h["num"])

    if h.get("alpha_lower"):
        parts.append(h["alpha_lower"])

    return ".".join(parts)