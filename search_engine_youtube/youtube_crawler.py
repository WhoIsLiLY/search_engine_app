import os
import sys
import requests
from dotenv import load_dotenv
import preprocessing
import similarity
import json

# Load file .env
load_dotenv()

# API Key YouTube
api_key = os.getenv('API_KEY')

# List of Dictionaries to save the result
results = []

# Keyword pencarian
keyword = "Terima kasih pak Jokowi"  # Ganti dengan keyword yang diinginkan
# keyword = " ".join(sys.argv[1:])
# keyword = preprocessing.stemmer_and_remove_stopwords(
#           preprocessing.preprocess_text(keyword)
#         )

# URL untuk pencarian video berdasarkan keyword
search_url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={requests.utils.quote(keyword)}&part=snippet&type=video&maxResults=5"

def display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity):
    result = {
        "source": "Youtube",
        "text_caption": original_text["caption"],
        "preprocessed_caption": preprocessed_text["caption"],
        "text_comments": original_text["comments"],
        "preprocessed_comments": preprocessed_text["comments"],
        "cosine_similarity": cosine_similarity,
        "asymetric_similarity": asymetric_similarity
    }
    results.append(result)

def fetch_youtube_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request Error: {e}")
        return {}

# Ambil video berdasarkan keyword
search_results = fetch_youtube_data(search_url)

if search_results.get('items'):
    for item in search_results['items']:
        original_text = {
            "caption": "",
            "comments": []
        }
        preprocessed_text = {
            "caption": "",
            "comments": []
        }
        video_id = item['id']['videoId']
        # title = item['snippet']['title']
        # channel_id = item['snippet']['channelId']
        # channel_title = item['snippet']['channelTitle']

        # Ambil detail video untuk deskripsi
        video_detail_url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&part=snippet"
        video_details = fetch_youtube_data(video_detail_url)

        if video_details.get('items'):
            original_description = video_details['items'][0]['snippet']['description']
            preprocessed_description = preprocessing.stemmer_and_remove_stopwords(
                                preprocessing.preprocess_text(original_description)
                            )
            original_text["caption"] = original_description
            preprocessed_text["caption"] = preprocessed_description
            # print(f"Description: {description}")

        # Ambil komentar utama
        comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&videoId={video_id}&part=snippet&maxResults=10"
        comments = fetch_youtube_data(comments_url)

        if comments.get('items'):
            for comment in comments['items']:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                preprocessed_comment = preprocessing.stemmer_and_remove_stopwords(
                                preprocessing.preprocess_text(comment_text)
                            )
                original_text["comments"].append(comment_text)
                preprocessed_text["comments"].append(preprocessed_comment)
                # print(f"- {comment_text}")
        else:
            print("No comments found")

        # Similarity
        cosine_similarity = similarity.calculateCosineSimilarity(preprocessed_text, keyword)
        asymetric_similarity = similarity.calculateAsymmetricSimilarity(preprocessed_text, keyword)

        # Bandingkan caption dan komentar terbaik
        display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity)
    
    # Send json
    json_output = json.dumps(results, ensure_ascii=False, indent=4)
    print(json_output)

else:
    print(f"No videos found for the keyword '{keyword}'.")