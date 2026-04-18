import fitz

from ingestion.normalize import (
    normalize_text,
    is_heading,
    extract_prefix,
    update_hierarchy,
    build_section_id,
    is_toc_line
)


def parse_pdf(file_path):

    doc = fitz.open(file_path)
    total_pages = len(doc)

    hierarchy = {"roman": "", "num": "", "alpha_upper": "", "alpha_lower": ""}

    records = []
    buffer = []

    current_section = {
        "section_id": "",
        "title": "",
        "text": "",
        "page": None
    }

    toc_mode = True

    for page_num in range(total_pages):

        page = doc.load_page(page_num)
        text = page.get_text("text")

        if not text:
            continue

        lines = text.split("\n")
        i = 0

        while i < len(lines):

            line = normalize_text(lines[i])

            if not line:
                i += 1
                continue

            # Skip TOC
            if toc_mode:
                if is_heading(line) and not is_toc_line(line):
                    toc_mode = False
                else:
                    i += 1
                    continue

            # Heading detection
            if is_heading(line):

                # 🔥 Merge multi-line heading (PDF only)
                full_heading = line
                j = i + 1

                while j < len(lines):

                    next_line = normalize_text(lines[j])

                    if not next_line:
                        j += 1
                        continue

                    if is_heading(next_line):
                        break

                    if next_line.endswith(".") and len(next_line.split()) > 8:
                        break

                    if not full_heading.endswith(".") and next_line[0].isupper():
                        full_heading += " " + next_line
                        j += 1
                    else:
                        break

                i = j - 1

                # Save previous section
                if buffer:
                    current_section["text"] = " ".join(buffer).strip()
                    records.append(current_section)
                    buffer = []

                prefix, title = extract_prefix(full_heading)

                hierarchy = update_hierarchy(hierarchy, prefix)
                section_id = build_section_id(hierarchy)

                current_section = {
                    "section_id": section_id,
                    "title": title,
                    "text": "",
                    "page": page_num + 1
                }

            else:
                buffer.append(line)

            i += 1

    # Final flush
    if buffer:
        current_section["text"] = " ".join(buffer).strip()
        records.append(current_section)

    return {
        "source_type": "pdf",
        "total_pages": total_pages,
        "total_sections": len(records),
        "sections": records
    }