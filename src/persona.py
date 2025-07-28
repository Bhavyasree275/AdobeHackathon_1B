def load_persona_job(persona_path, job_path):
    """
    Load persona and job-to-be-done text from files.

    Args:
        persona_path (str): Path to the persona description file (JSON or plain text).
        job_path (str): Path to the job-to-be-done description file (plain text).

    Returns:
        tuple: (persona_text, job_text) both as strings.
    """
    with open(persona_path, 'r', encoding='utf-8') as f:
        persona_text = f.read().strip()

    with open(job_path, 'r', encoding='utf-8') as f:
        job_text = f.read().strip()

    return persona_text, job_text
