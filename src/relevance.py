from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections(sections, persona_text, job_text):
    """
    Rank document sections by their relevance to the combined persona and job description.

    Args:
        sections (list of dict): List of dicts, each with keys like 'section_title' and 'section_text'.
        persona_text (str): Text describing the persona.
        job_text (str): Text describing the job to be done.

    Returns:
        List of sections sorted by relevance score (highest first). Each section dict
        will have an added 'score' key with the relevance score.
    """
    # Combine persona and job texts to form the query for ranking
    combined_query = persona_text + " " + job_text

    # Prepare section texts by concatenating title and text for ranking
    section_texts = [
        sec.get("section_title", "") + " " + sec.get("section_text", "") 
        for sec in sections
    ]

    # Fit TF-IDF vectorizer on all sections plus the combined query
    vectorizer = TfidfVectorizer(stop_words='english').fit(section_texts + [combined_query])

    # Transform sections and query to TF-IDF vectors
    section_vecs = vectorizer.transform(section_texts)
    query_vec = vectorizer.transform([combined_query])

    # Compute cosine similarity between each section and the query
    similarities = cosine_similarity(section_vecs, query_vec).flatten()

    # Add score to each section
    for i, section in enumerate(sections):
        section["score"] = similarities[i]

    # Sort sections by descending score
    ranked_sections = sorted(sections, key=lambda x: x["score"], reverse=True)

    return ranked_sections


