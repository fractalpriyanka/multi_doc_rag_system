from bs4 import BeautifulSoup
from ingestion.fetch_doc import fetch_google_doc_html
from ingestion.normalize import (
    normalize_text,
    is_heading,
    extract_prefix,
    update_hierarchy,
    build_section_id
)


def process_google_doc(url, raw_path):

    html = fetch_google_doc_html(url, raw_path)
    soup = BeautifulSoup(html, "lxml")

    elements = soup.find_all(["p", "div"])

    hierarchy = {"roman": "", "num": "", "alpha_upper": "", "alpha_lower": ""}

    records = []
    buffer = []
    current = {"section_id": "", "title": "", "text": ""}

    for el in elements:

        text = normalize_text(el.get_text())

        if not text:
            continue

        # GDoc → no aggressive merging
        if is_heading(text):

            if buffer:
                current["text"] = " ".join(buffer)
                records.append(current)
                buffer = []

            prefix, title = extract_prefix(text)

            hierarchy = update_hierarchy(hierarchy, prefix)
            sec_id = build_section_id(hierarchy)

            current = {
                "section_id": sec_id,
                "title": title,
                "text": ""
            }

        else:
            buffer.append(text)

    if buffer:
        current["text"] = " ".join(buffer)
        records.append(current)

    return {
        "source_type": "google_doc",
        "sections": records
    }