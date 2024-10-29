import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-gpu")  # Applicable to Windows
chrome_options.add_argument("start-maximized")  # Start maximized
chrome_options.add_argument("disable-infobars")  # Disable infobars
chrome_options.add_argument("--disable-extensions")  # Disable extensions

# Initialize WebDriver with options
wd = webdriver.Chrome(options=chrome_options)

# Get search query from arguments
keyword = sys.argv[1]
wd.get("https://www.youtube.com/results?search_query=" + keyword)

# Wait until videos are loaded
WebDriverWait(wd, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer'))
)

# Collect top 10 video links
video_links = []
videos = wd.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')[:10]
for video in videos:
    video_url = video.find_element(By.ID, 'thumbnail').get_attribute('href')
    video_links.append(video_url) 
 # print(video_links) # sampai sini sudah benar, dapat 10 link videos

for idx, link in enumerate(video_links):
    wd.get(link)
    # Mute the YouTube video audio using JavaScript
    try:
      wd.execute_script("""
          let video = document.querySelector('video');
          if (video) {
              video.muted = true;
              video.volume = 0;
          }
        """)
    except:
        print("Unable to mute video")

    # Get video title and description
    try:
        title = wd.find_element(By.CSS_SELECTOR, 'yt-formatted-string').text
    except:
        title = "No title found"

    try:
        descriptions = wd.find_elements(By.CSS_SELECTOR, "span.yt-core-attributed-string--link-inherit-color").text
    except:
        description = "No description available"

    print(f"{idx+1}. {title.encode('utf-8', errors='replace').decode('utf-8')}")
    print(f"Description: {description}\n")

    # Scroll down to load comments
    wd.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    #time.sleep(5)

    WebDriverWait(wd, 10).until(
      EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#content #content-text'))
    )
    # Get top 10 comments
    comments = wd.find_elements(By.CSS_SELECTOR, "#content #content-text")[:10]
    for comment_idx, comment in enumerate(comments):
        comment_text = comment.text
        print(f"   Comment {comment_idx+1}: {comment_text}")

        # Expand replies if available
        try:
            show_replies_button = comment.find_element(By.XPATH, "../../following-sibling::ytd-comment-replies-renderer//tp-yt-paper-button")
            wd.execute_script("arguments[0].click();", show_replies_button)
            time.sleep(5)

            # Get up to 10 replies
            replies = comment.find_elements(By.XPATH, "../../following-sibling::ytd-comment-replies-renderer//ytd-comment-renderer #content-text")[:10]
            for reply_idx, reply in enumerate(replies):
                reply_text = reply.text
                print(f"      Reply {reply_idx+1}: {reply_text}")

        except:
            print("      No replies found")

wd.quit()
"""
import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-gpu")  # Applicable to Windows
chrome_options.add_argument("start-maximized")  # Start maximized
chrome_options.add_argument("disable-infobars")  # Disable infobars
chrome_options.add_argument("--disable-extensions")  # Disable extensions

# Initialize WebDriver with options
wd = webdriver.Chrome(options=chrome_options)

# Get search query from arguments
keyword = sys.argv[1]
wd.get("https://www.youtube.com/results?search_query=" + keyword)

# Wait until videos are loaded
WebDriverWait(wd, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ytd-video-renderer'))
)

# Set up counters and parameters for scrolling
i = 0
scroll_attempts = 0
max_scroll_attempts = 5  # Maximum scroll attempts to limit infinite scrolling

while i < 10 and scroll_attempts < max_scroll_attempts:
    # Get current video elements
    videos = wd.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')
    
    # Iterate over videos and print titles
    for video in videos[i:]:
        if i >= 10:  # Stop if 10 titles are collected
            break
        try:
            title = video.find_element(By.CSS_SELECTOR, 'yt-formatted-string').text
            print(f"{i+1}. {title.encode('utf-8', errors='replace').decode('utf-8')}")
        except Exception as e:
            print(f"Could not retrieve title for video {i+1}: {e}")
        i += 1
    
    # Scroll down to load more videos
    wd.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)  # Wait for more content to load
    scroll_attempts += 1  # Increase scroll attempt counter

wd.quit()"""

""" USING YOUTUBE API v3
import requests

API_KEY = 'YOUR_YOUTUBE_API_KEY'  # Replace with your actual API key
query = 'Re:ZERO -Starting Life in Another World- Season 3'
max_results = 10

# Step 1: Search for videos
search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={query}&key={API_KEY}&type=video"
search_response = requests.get(search_url).json()

for idx, item in enumerate(search_response.get('items', [])):
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    
    # Step 2: Get video description
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
    video_response = requests.get(video_url).json()
    description = video_response['items'][0]['snippet'].get('description', 'No description available')

    print(f"{idx+1}. Title: {title}")
    print(f"   Description: {description}\n")

    # Step 3: Retrieve top 10 comments and replies
    comments_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults=10&key={API_KEY}"
    comments_response = requests.get(comments_url).json()
    
    for comment_idx, comment_thread in enumerate(comments_response.get('items', [])):
        top_comment = comment_thread['snippet']['topLevelComment']['snippet']
        comment_text = top_comment['textDisplay']
        author = top_comment['authorDisplayName']
        
        print(f"   Comment {comment_idx+1} by {author}: {comment_text}")

        # Step 4: Retrieve replies to the top-level comment, if available
        if comment_thread['snippet']['totalReplyCount'] > 0:
            comment_id = comment_thread['id']
            replies_url = f"https://www.googleapis.com/youtube/v3/comments?part=snippet&parentId={comment_id}&maxResults=10&key={API_KEY}"
            replies_response = requests.get(replies_url).json()
            
            for reply_idx, reply in enumerate(replies_response.get('items', [])):
                reply_text = reply['snippet']['textDisplay']
                reply_author = reply['snippet']['authorDisplayName']
                
                print(f"      Reply {reply_idx+1} by {reply_author}: {reply_text}")

    print("\n" + "="*50 + "\n")

"""