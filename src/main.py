import sys
import json
import datetime
from document_parser import extract_sections
from persona import load_persona_job
from relevance import rank_sections

def main():
    if len(sys.argv) != 5:
        print("Usage: main.py <input_pdf> <output_json> <persona_file> <job_file>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_json = sys.argv[2]
    persona_file = sys.argv[3]
    job_file = sys.argv[4]

    print(f"Processing PDF: {input_pdf}")
    sections = extract_sections(input_pdf)

    print("Loading persona and job descriptions...")
    persona_text, job_text = load_persona_job(persona_file, job_file)

    print("Ranking sections relevance...")
    ranked_sections = rank_sections(sections, persona_text, job_text)

    # Prepare output JSON structure
    output = {
        "metadata": {
            "input_documents": [input_pdf],
            "persona": persona_text,
            "job_to_be_done": job_text,
            "processing_timestamp": datetime.datetime.utcnow().isoformat()
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    # Fill extracted_sections list (assign importance_rank)
    for idx, sec in enumerate(ranked_sections, start=1):
        output["extracted_sections"].append({
            "document": sec["document"],
            "page_number": sec["page"],
            "section_title": sec["section_title"],
            "importance_rank": idx
        })

    # For demo, we'll send section text as subsection analysis directly (can be enhanced)
    for sec in ranked_sections:
        output["sub_section_analysis"].append({
            "document": sec["document"],
            "page_number": sec["page"],
            "refined_text": sec["section_text"]
        })

    # Save output JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Output written to: {output_json}")

if __name__ == "__main__":
    main()
