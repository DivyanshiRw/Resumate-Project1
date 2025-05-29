import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import language_tool_python

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9 ]+', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    stop_words -= {'more', 'most', 'less', 'not', 'very'}  # keep meaningful words
    return ' '.join([t for t in tokens if t not in stop_words])

def check_resume_sections(text):
    sections = ['skills', 'experience', 'education', 'projects']
    bonus = ['certifications', 'awards', 'achievements', 'hackathons']
    text = text.lower()
    section_found = {s: s in text for s in sections + bonus}
    core_score = sum(section_found[s] for s in sections) / len(sections) * 100
    bonus_score = sum(section_found[s] for s in bonus) / len(bonus) * 5  # total bonus weight: 5%
    return round(core_score + bonus_score, 2), section_found

def check_contact_info(text):
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    linkedin_match = re.search(r'linkedin\.com\/(in|pub)\/[\w\-]+', text.lower()) or 'linkedin' in text.lower()
    score = 100 if email_match and linkedin_match else 50 if email_match or linkedin_match else 0
    return score, {
        'email_present': bool(email_match),
        'linkedin_present': bool(linkedin_match)
    }

def check_metrics(text):
    patterns = [
        r'\d+%', r'\$\d+[kKmM]?', r'\d+\+?\s+(years|projects|clients|teams)',
        r'increased\s+\w+\s+by\s+\d+%', r'\d+\s+(certifications|awards|publications)'
    ]
    matches = sum(len(re.findall(p, text.lower())) for p in patterns)
    return min(matches * 10, 100), matches

def check_grammar(text):
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    matches = tool.check(text)
    words = len(text.split())
    error_rate = len(matches) / words if words else 0
    score = max(100 - error_rate * 300, 70)  # less strict penalty
    return round(score, 2), len(matches)

def check_length(text):
    words = len(text.split())
    if 300 <= words <= 950:
        return 100, words
    elif 250 <= words < 300 or 950 < words <= 1100:
        return 80, words
    else:
        return 60, words

def jd_match_score(resume_text, jd_text):
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([cleaned_resume, cleaned_jd])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)

def compute_resume_score(resume_text, job_desc=None):
    # Core evaluations
    section_score, section_info = check_resume_sections(resume_text)
    contact_score, contact_info = check_contact_info(resume_text)
    metric_score, metric_count = check_metrics(resume_text)
    grammar_score, grammar_issues = check_grammar(resume_text)
    length_score, word_count = check_length(resume_text)
    jd_score = jd_match_score(resume_text, job_desc) if job_desc else None

    # Weights
    weights = {
        'section': 0.25,
        'contact': 0.15,
        'metric': 0.15,
        'grammar': 0.10,
        'length': 0.15,
        'jd': 0.20 if jd_score is not None else 0.0
    }

        # Compute weighted raw score
    raw_score = (
        weights['section'] * section_score +
        weights['contact'] * contact_score +
        weights['metric'] * metric_score +
        weights['grammar'] * grammar_score +
        weights['length'] * length_score +
        (weights['jd'] * jd_score if jd_score is not None else 0)
    )

    # Sum of weights actually used
    used_weights = {
        k: v for k, v in weights.items()
        if k != 'jd' or jd_score is not None
    }
    total_used_weight = sum(used_weights.values())

    # Normalize final score to 100 scale
    total_score = round((raw_score / total_used_weight), 2)
    total_score = min(total_score, 100)


    # Quality label
    if total_score >= 85:
        quality = "Excellent ✅"
    elif total_score >= 70:
        quality = "Good 👍"
    elif total_score >= 55:
        quality = "Fair ⚠️"
    else:
        quality = "Needs Improvement ❌"

    # Suggestions
    suggestions = []
    if section_score < 90:
        suggestions.append("Include all core sections: Skills, Experience, Projects, Education.")
    if not contact_info['email_present'] or not contact_info['linkedin_present']:
        suggestions.append("Make sure email and LinkedIn are clearly visible.")
    if metric_score < 40:
        suggestions.append("Add more quantifiable achievements.")
    if grammar_score < 80:
        suggestions.append("Fix grammatical and spelling errors.")
    if not (300 <= word_count <= 950):
        suggestions.append("Resume should ideally be 300–950 words for better ATS readability.")
    if not suggestions:
        suggestions.append("Great job! Your resume looks ATS-ready.")

    return {
        "score": total_score,
        "quality": quality,
        "breakdown": {
            "section_score": section_score,
            "contact_score": contact_score,
            "metric_score": metric_score,
            "grammar_score": grammar_score,
            "length_score": length_score,
            "jd_score": jd_score
        },
        "details": {
            "sections_found": section_info,
            "contact_info": contact_info,
            "metric_count": metric_count,
            "grammar_issues": grammar_issues,
            "word_count": word_count
        },
        "suggestions": suggestions
    }
