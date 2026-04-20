from flask import Blueprint, request, jsonify
import pickle
import pandas as pd
from preprocessing.cleaner import clean_text
from sklearn.metrics.pairwise import cosine_similarity

match_bp = Blueprint('match', __name__)

# Load models
with open('models/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = pickle.load(f)

with open('models/job_vectors.pkl', 'rb') as f:
    job_vectors = pickle.load(f)

df_jobs = pd.read_csv('data/cleaned_jobs_unique.csv')

@match_bp.route('/match', methods=['POST'])
def match():
    data = request.get_json()
    resume_text = data.get('resume', '')

    if not resume_text:
        return jsonify({'error': 'No resume text provided'}), 400

    cleaned_resume = clean_text(resume_text)
    resume_vec = tfidf.transform([cleaned_resume])
    scores = cosine_similarity(resume_vec, job_vectors)[0]
    top_indices = scores.argsort()[::-1][:5]

    results = []
    for i in top_indices:
        results.append({
            'job_title': df_jobs['Job Title'][i],
            'score': round(scores[i] * 100, 2)
        })

    return jsonify({'matches': results})