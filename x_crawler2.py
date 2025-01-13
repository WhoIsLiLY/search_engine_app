import tweepy
import os
import dotenv
import json
import sys
import preprocessing
import similarity
from datetime import datetime, timezone
from typing import List, Dict

class XCrawler:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        """
        Initialize X API crawler with authentication credentials
        """
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def search_tweets(self, keyword: str, max_results: int = 2) -> List[Dict]:
        """
        Search for tweets containing images with the given keyword
        """
        results = []
        
        # Search query parameters
        query = f"{keyword} has:images -is:retweet"
        
        try:
            # Search tweets
            tweets = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics'],
                expansions=['author_id'],
                media_fields=['url']
            )

            if not tweets.data:
                print("No tweets found")
                return results

            for tweet in tweets.data:
                # Get original text
                original_text = {
                    "caption": tweet.text,
                    "comments": []
                }

                # Preprocess text
                preprocessed_text = {
                    "caption": preprocessing.stemmer_and_remove_stopwords(
                        preprocessing.preprocess_text(tweet.text)
                    ),
                    "comments": []
                }

                # Get comments (replies)
                replies = self.client.search_recent_tweets(
                    query=f"conversation_id:{tweet.id}",
                    max_results=10,
                    tweet_fields=['in_reply_to_tweet_id']
                )

                if replies.data:
                    for reply in replies.data:
                        original_text["comments"].append(reply.text)
                        preprocessed_text["comments"].append(
                            preprocessing.stemmer_and_remove_stopwords(
                                preprocessing.preprocess_text(reply.text)
                            )
                        )

                # Calculate similarities
                preprocessed_keyword = preprocessing.stemmer_and_remove_stopwords(
                    preprocessing.preprocess_text(keyword)
                )
                
                cosine_similarity = similarity.calculateCosineSimilarity(
                    preprocessed_text, 
                    preprocessed_keyword
                )
                asymetric_similarity = similarity.calculateAsymmetricSimilarity(
                    preprocessed_text, 
                    preprocessed_keyword
                )

                # Create result dictionary
                result = {
                    "source": "X",
                    "text_caption": original_text["caption"],
                    "preprocessed_caption": preprocessed_text["caption"],
                    "text_comments": original_text["comments"],
                    "preprocessed_comments": preprocessed_text["comments"],
                    "cosine_similarity": cosine_similarity,
                    "asymetric_similarity": asymetric_similarity
                }
                
                results.append(result)

        except Exception as e:
            print(f"An error occurred: {e}")

        return results

def main():
    # Load credentials from .env file
    dotenv.load_dotenv()

    API_KEY = os.getenv('X_API_KEY')
    API_SECRET = os.getenv('X_API_SECRET')
    ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')

    # Get search keyword from command line arguments
    keyword = " ".join(sys.argv[1:])
    if not keyword:
        print("Please provide a search keyword")
        sys.exit(1)

    # Initialize crawler
    crawler = XCrawler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Perform search
    results = crawler.search_tweets(keyword)

    # Output results as JSON
    print(json.dumps(results, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()