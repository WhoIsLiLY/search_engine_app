from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculateCosineSimilarity(preprocessed_text, keyword):
    # Extract all texts into a list
    documents = []
    if preprocessed_text["caption"]:
        documents.append(preprocessed_text["caption"])
        
    documents.extend(preprocessed_text["comments"]) # ["a", "b"] ["a", "b", "c"]
    
    if not documents:  # If no documents exist
        return 0
    
    # Add keyword as the last document
    documents.append(keyword)
    
    # Create TF-IDF representation
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity for each document with the keyword
    # Keyword is the last document in the matrix
    similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1])
    
    # Return the maximum similarity found
    return np.round(np.max(similarities), 2)

def calculateAsymmetricSimilarity(preprocessed_text, keyword):
    # Extract all texts into a list
    documents = []
    if preprocessed_text["caption"]:
        documents.append(preprocessed_text["caption"])
    documents.extend(preprocessed_text["comments"])
    
    if not documents:  # If no documents exist
        return 0
    
    max_asymmetric_sim = 0.0
    
    for doc in documents:
        # Create TF-IDF representation for current document and keyword
        data = [doc, keyword]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(data).toarray()
        
        # Calculate asymmetric similarity
        numerator = np.sum(np.minimum(tfidf_matrix[0], tfidf_matrix[1]))
        denominator = np.sum(tfidf_matrix[0])
        
        asymmetric_sim = numerator / denominator if denominator != 0 else 0
        max_asymmetric_sim = max(max_asymmetric_sim, asymmetric_sim)
    
    return np.round(max_asymmetric_sim, 2)


# def calculateCosineSimilarity(preprocessed_text, keyword):
#     # Gabungkan teks preprocessed text dan keyword
#     data = [preprocessed_text, keyword]
    
#     # Buat representasi TF-IDF
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(data)
    
#     # Hitung cosine similarity
#     cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    
#     # Return hasil dalam bentuk string
#     return np.round(cosine_sim[0][0], 2)

# def calculateAsymmetricSimilarity(preprocessed_text, keyword):
#     data = [preprocessed_text, keyword]

#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(data).toarray()

#     numerator = np.sum(np.minimum(tfidf_matrix[0], tfidf_matrix[1]))
#     denominator = np.sum(tfidf_matrix[0])

#     asymmetric_sim = numerator / denominator if denominator != 0 else 0

#     return np.round(asymmetric_sim, 2)

# query = 5
# doc_gabungan = 10
# doc1 = 3
# doc2 = 5
# doc3= 2

# min(5, 10) = 5

# sum(min(5, 3)+min(5,5)+min(5,2)) = 10

# query = 3
# doc_gabungan = 20
# doc1 = 3
# doc2 = 5
# doc3= 2
# doc4 = 3
# doc5 = 5
# doc6= 2

# min(5, 10) = 5

# sum(min(5, 3)+min(5,5)+min(5,2))