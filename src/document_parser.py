import fitz  # PyMuPDF

def extract_sections(pdf_path):
    """
    Extract sections from a PDF by detecting headings via font size and bold style.
    Returns a list of dicts with keys:
      - document: filename
      - page: 1-based page number
      - section_title: heading text
      - section_text: accumulated section content (string)
    """
    doc = fitz.open(pdf_path)
    sections = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue

                    size = span["size"]
                    flags = span["flags"]
                    is_bold = bool(flags & 2)  # font flag: 2 = bold

                    # Heuristic: size > 12 or bold == heading
                    if size > 12 or is_bold:
                        sections.append({
                            "document": pdf_path.split('/')[-1],
                            "page": page_num + 1,
                            "section_title": text,
                            "section_text": ""
                        })
                    else:
                        if sections:
                            sections[-1]["section_text"] += " " + text
                        else:
                            # Default section if no heading yet
                            sections.append({
                                "document": pdf_path.split('/')[-1],
                                "page": page_num + 1,
                                "section_title": "Introduction",
                                "section_text": text
                            })
    return sections
