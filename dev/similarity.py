from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def calculateCosineSimilarity(preprocessed_text, keyword):
    # Gabungkan teks preprocessed text dan keyword
    data = [preprocessed_text, keyword]
    
    # Buat representasi TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data)
    
    # Hitung cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    
    # Return hasil dalam bentuk string
    return np.round(cosine_sim[0][0], 2)

def calculateAsymmetricSimilarity(preprocessed_text, keyword):
    data = [preprocessed_text, keyword]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data).toarray()

    numerator = np.sum(np.minimum(tfidf_matrix[0], tfidf_matrix[1]))
    denominator = np.sum(tfidf_matrix[0])

    asymmetric_sim = numerator / denominator if denominator != 0 else 0

    return np.round(asymmetric_sim, 2)
