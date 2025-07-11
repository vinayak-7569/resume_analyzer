from flask import Blueprint, request, render_template, jsonify
from .utils import extract_text_from_pdf
from .nlp_extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_education,
    match_job_skills,
    generate_suggestions,
    extract_experience  # Optional
)

bp = Blueprint('analyzer', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    if file.filename.strip() == '':
        return jsonify({'error': 'No selected file'}), 400

    text = extract_text_from_pdf(file)
    if text.startswith("Error"):
        return jsonify({'error': text}), 500

    name = extract_name(text) or "N/A"
    email = extract_email(text) or "N/A"
    phone = extract_phone(text) or "N/A"
    skills = extract_skills(text) or []
    education = extract_education(text) or []
    experience = extract_experience(text) or []

    word_count = len(text.split())

    job_description = request.form.get('job_description', '')
    job_keywords = extract_skills(job_description) if job_description else []

    match_score, matched_skills = match_job_skills(skills, job_keywords)
    suggestions = generate_suggestions(job_keywords, skills, text) if job_keywords else []

    total_score = 0
    weights = {
        'skills': 0.6,
        'education': 0.2,
        'experience': 0.2
    }
    total_score += match_score * weights['skills']
    if education: total_score += 20 * weights['education']
    if experience: total_score += 20 * weights['experience']

    final_score = round(min(total_score, 100), 2)

    response = {
        'status': 'Success',
        'file_name': file.filename,
        'word_count': word_count,
        'name': name,
        'email': email,
        'phone': phone,
        'education': education,
        'experience': experience,
        'skills': skills,
        'matched_skills': matched_skills,
        'match_score': match_score,
        'final_score': final_score,
        'raw_text_preview': text[:1000],
        'suggestions': suggestions,
        'feedback_summary': generate_feedback_summary(final_score)
    }

    return jsonify(response)

def generate_feedback_summary(score):
    if score >= 85:
        return "Excellent fit for the job. Well-matched resume."
    elif score >= 70:
        return "Good match. A few improvements can enhance your chances."
    elif score >= 50:
        return "Average match. Consider adding more relevant skills or details."
    else:
        return "Low match. Resume lacks many required job qualifications."
