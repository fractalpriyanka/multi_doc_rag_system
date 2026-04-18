from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from ingestion.normalize import (
    normalize_text,
    is_heading,
    extract_prefix,
    update_hierarchy,
    build_section_id
)


# 🔥 Helper to iterate in order (paragraph + table)
def iter_block_items(parent):
    for child in parent.element.body:
        if child.tag.endswith('p'):
            yield Paragraph(child, parent)
        elif child.tag.endswith('tbl'):
            yield Table(child, parent)


def parse_docx(file_path):

    doc = Document(file_path)

    hierarchy = {"roman": "", "num": "", "alpha_upper": "", "alpha_lower": ""}

    records = []
    buffer = []

    current_section = {
        "section_id": "",
        "title": "",
        "text": ""
    }

    # 🔥 Iterate in correct order (important)
    for block in iter_block_items(doc):

        # ---------- PARAGRAPH ----------
        if isinstance(block, Paragraph):

            text = normalize_text(block.text)

            if not text:
                continue

            if block.style.name.startswith("Heading") or is_heading(text):

                # save previous section
                if buffer:
                    current_section["text"] = " ".join(buffer).strip()
                    records.append(current_section)
                    buffer = []

                prefix, title = extract_prefix(text)

                hierarchy = update_hierarchy(hierarchy, prefix)
                section_id = build_section_id(hierarchy)

                current_section = {
                    "section_id": section_id,
                    "title": title,
                    "text": ""
                }

            else:
                buffer.append(text)

        # ---------- TABLE ----------
        elif isinstance(block, Table):

            table_text = []

            for row in block.rows:
                row_text = " | ".join(
                    normalize_text(cell.text)
                    for cell in row.cells
                    if cell.text.strip()
                )
                if row_text:
                    table_text.append(row_text)

            if table_text:
                # 🔥 attach table to current section
                buffer.append("[TABLE] " + " || ".join(table_text))

    # 🔹 Final flush
    if buffer:
        current_section["text"] = " ".join(buffer).strip()
        records.append(current_section)

    return {
        "source_type": "docx",
        "total_sections": len(records),
        "sections": records
    }