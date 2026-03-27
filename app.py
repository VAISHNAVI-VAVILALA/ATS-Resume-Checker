from flask import Flask, render_template, request
import google.generativeai as genai
from utils import extract_text_from_pdf, calculate_ats_score

app = Flask(__name__)

#  Replace with your Gemini API Key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['resume']
    job_desc = request.form['job_desc']

    resume_text = extract_text_from_pdf(file)

    score, missing_keywords = calculate_ats_score(resume_text, job_desc)

    # AI Suggestions using Gemini
    prompt = f"""
    Analyze this resume against the job description.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_desc}
    
    Give:
    1. Improvement suggestions
    2. Missing skills
    3. Formatting tips
    """

    response = model.generate_content(prompt)

    return render_template(
        "index.html",
        score=score,
        missing=missing_keywords,
        suggestions=response.text
    )


if __name__ == '__main__':
    app.run(debug=True)