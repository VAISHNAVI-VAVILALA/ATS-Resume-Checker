from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def calculate_ats_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    jd_words = set(job_desc.lower().split())

    matched = resume_words.intersection(jd_words)

    if len(jd_words) == 0:
        return 0, []

    score = (len(matched) / len(jd_words)) * 100

    missing_keywords = jd_words - resume_words

    return round(score, 2), list(missing_keywords)[:10]