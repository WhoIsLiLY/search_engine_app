import os
import sys
import requests
from dotenv import load_dotenv
import preprocessing

# Load file .env
load_dotenv()

# API Key YouTube
api_key = os.getenv('API_KEY')

# Keyword pencarian
keyword = "Terima kasih pak Jokowi"  # Ganti dengan keyword yang diinginkan
keyword = " ".join(sys.argv[1:])
keyword = preprocessing.stemmer_and_remove_stopwords(
          preprocessing.preprocess_text(keyword)
        )

# URL untuk pencarian video berdasarkan keyword
search_url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&q={requests.utils.quote(keyword)}&part=snippet&type=video&maxResults=10"

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
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['channelTitle']

        print(f"Video Title: {title}")
        print(f"Channel: {channel_title}")

        # Ambil detail video untuk deskripsi
        video_detail_url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_id}&part=snippet"
        video_details = fetch_youtube_data(video_detail_url)

        if video_details.get('items'):
            description = video_details['items'][0]['snippet']['description']
            print(f"Description: {description}")

        # Ambil komentar utama
        comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&videoId={video_id}&part=snippet&maxResults=5"
        comments = fetch_youtube_data(comments_url)

        print("Comments:")
        if comments.get('items'):
            for comment in comments['items']:
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                print(f"- {comment_text}")
        else:
            print("No comments found.")

        print("=============================")
else:
    print(f"No videos found for the keyword '{keyword}'.")
