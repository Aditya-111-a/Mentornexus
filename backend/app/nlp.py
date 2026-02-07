from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ResearchSimilarityEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def fit(self, faculty_texts: list):
        self.faculty_vectors = self.vectorizer.fit_transform(faculty_texts)

    def compute(self, student_text: str):
        student_vec = self.vectorizer.transform([student_text])
        scores = cosine_similarity(student_vec, self.faculty_vectors)[0]
        return scores.tolist()
