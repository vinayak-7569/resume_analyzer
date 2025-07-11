import re
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise Exception("spaCy model not found. Run: python -m spacy download en_core_web_sm")

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return "Not found"

def extract_email(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0).strip() if match else "Not found"

def extract_phone(text):
    match = re.search(r'\b(?:\+91[-\s]?|0)?[6-9]\d{9}\b', text)
    return match.group(0).strip() if match else "Not found"

def extract_skills(text):
    skill_keywords = [
        'python', 'java', 'c++', 'c', 'html', 'css', 'javascript', 'react', 'node.js',
        'machine learning', 'deep learning', 'nlp', 'flask', 'django', 'sql',
        'pandas', 'numpy', 'tensorflow', 'keras', 'git', 'github', 'linux',
        'data analysis', 'power bi', 'excel', 'matplotlib', 'seaborn', 'spark'
    ]
    text_lower = text.lower()
    found_skills = [skill for skill in skill_keywords if skill in text_lower]
    return list(set(found_skills)) if found_skills else ["No recognizable skills"]

def extract_education(text):
    education_keywords = [
        'b.tech', 'm.tech', 'b.sc', 'm.sc', 'bca', 'mca', 'ph.d', 'b.e', 'm.e',
        'bachelor of technology', 'master of technology', 'bachelor of science',
        'master of science', 'bachelor of computer applications', 'master of computer applications',
        'mba', 'bba', 'diploma', '12th', '10th'
    ]
    text_lower = text.lower()
    matches = [kw.upper() for kw in education_keywords if kw in text_lower]
    return list(set(matches)) if matches else ["Not found"]

def extract_experience(text):
    lines = text.split('\n')
    experience_keywords = ['experience', 'intern', 'company', 'worked at', 'position', 'role', 'project']
    extracted = [line.strip() for line in lines if any(k in line.lower() for k in experience_keywords)]
    return extracted[:10] if extracted else []

def match_job_skills(resume_skills, job_skills):
    resume_set = set(skill.lower() for skill in resume_skills)
    job_set = set(skill.lower() for skill in job_skills)
    matched = list(resume_set & job_set)
    score = (len(matched) / len(job_set)) * 100 if job_set else 0
    return round(score, 2), matched

def generate_suggestions(jd_keywords, resume_skills, resume_text):
    suggestions = []
    resume_set = set(skill.lower() for skill in resume_skills)
    jd_set = set(skill.lower() for skill in jd_keywords)
    missing_skills = jd_set - resume_set
    for skill in missing_skills:
        suggestions.append(f"Consider adding or highlighting experience with '{skill}' to match the job description.")

    soft_skills = {
        "team": "Mention any teamwork or collaboration experience.",
        "project": "Add or emphasize relevant projects that align with the job role.",
        "communication": "Highlight communication or presentation experience.",
        "leadership": "Include leadership experience from academics, clubs, or internships.",
    }
    resume_text_lower = resume_text.lower()
    for soft_skill, tip in soft_skills.items():
        if soft_skill in " ".join(jd_keywords).lower() and soft_skill not in resume_text_lower:
            suggestions.append(tip)

    return suggestions if suggestions else ["Your resume is well-aligned with the job description."]
