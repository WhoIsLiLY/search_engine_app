import sys
import json
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import preprocessing  # Import preprocessing.py
import similarity

# Handle encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Validate keyword argument
# if len(sys.argv) < 2:
#     print("Error: Keyword argument is missing. Usage: python instagram_crawler.py <keyword>")
#     sys.exit(1)

# List of Dictionaries to save the result
results = []

# Combine all keyword arguments into a single string
keyword = " ".join(sys.argv[1:])
keyword = preprocessing.stemmer_and_remove_stopwords(
          preprocessing.preprocess_text(keyword)
        )

# Setup Selenium Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
# Uncomment for headless mode
# chrome_options.add_argument("--headless")

# Initialize WebDriver
try:
    wd = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
    sys.exit(1)

# # Instagram login
# username = "dummy_ig_iir"  # Replace with your Instagram username
# password = "dummyinstagram"  # Replace with your Instagram password

# try:
#     wd.get("https://www.instagram.com/accounts/login/")
#     WebDriverWait(wd, 30).until(EC.presence_of_element_located((By.NAME, "username")))

#     wd.find_element(By.NAME, "username").send_keys(username)
#     wd.find_element(By.NAME, "password").send_keys(password)

#     login_button = WebDriverWait(wd, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in') or contains(., 'Masuk')]"))
#     )
#     login_button.click()

#     WebDriverWait(wd, 30).until(EC.url_changes("https://www.instagram.com/accounts/login/"))
# except Exception as e:
#     print(f"Failed to log in: {e}")
#     wd.quit()
#     sys.exit(1)

# Search Instagram posts on Google
query = "site:instagram.com+inurl:/p/+" + keyword
google_links = []
seen_links = set()
start = 0

while len(google_links) < 1:
    google_search_url = f"https://www.google.com/search?q={query}&start={start}"
    wd.get(google_search_url)
    time.sleep(3)

    try:
        google_results = wd.find_elements(By.CSS_SELECTOR, 'div.MjjYud a')
        for result in google_results:
            link = result.get_attribute('href')
            if "/p/" in link and "instagram.com" in link and link not in seen_links:
                google_links.append(link)
                seen_links.add(link)
                if len(google_links) >= 1:
                    break
    except Exception as e:
        print(f"Error fetching Google results: {e}")

    start += 10
    if len(google_results) == 0:
        break

if not google_links:
    print("No Instagram post links found.")
    wd.quit()
    sys.exit(1)

# Display results
def display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity):
    result = {
        "source": "Instagram",
        "text_caption": original_text["caption"],
        "preprocessed_caption": preprocessed_text["caption"],
        "text_comments": original_text["comments"],
        "preprocessed_comments": preprocessed_text["comments"],
        "cosine_similarity": cosine_similarity,
        "asymetric_similarity": asymetric_similarity
    }
    results.append(result)

for idx, link in enumerate(google_links):
    wd.get(link)
    time.sleep(2)

    original_text = {
        "caption": "",
        "comments": []
    }
    preprocessed_text = {
        "caption": "",
        "comments": []
    }
 
    # # Get account name
    # try:
    #     account = WebDriverWait(wd, 10).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, "span.x1vvkbs"))
    #     ).text
    # except:
    #     account = "Account not available"

    # Get caption
    try:
        WebDriverWait(wd, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1._aade")))
        original_caption =  wd.find_element(By.CSS_SELECTOR, "h1._aade").text
        preprocessed_caption = preprocessing.stemmer_and_remove_stopwords(
            preprocessing.preprocess_text(original_caption)
        )
    except:
        original_caption = ""
        preprocessed_caption = ""
    
    original_text["caption"] = original_caption
    preprocessed_text["caption"] = preprocessed_caption
    
    # Get comments
    try:
        original_comments = []
        preprocessed_comments = []
        wait = WebDriverWait(wd, 10)  # Tunggu maksimal 10 detik

        while len(original_comments) < 10:  # Loop hingga setidaknya 10 komentar diambil
            # Tunggu hingga elemen komentar tersedia
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul._a9ym li span._aaco")))
            current_comments = wd.find_elements(By.CSS_SELECTOR, "ul._a9ym li span._aaco")

            for comment in current_comments:
                comment_text = comment.text.strip()
                if comment_text not in original_comments:
                    keyword_list = keyword.split()
                    preprocessed_comment = preprocessing.stemmer_and_remove_stopwords(preprocessing.preprocess_text(comment_text))
                    
                    # Cek apakah ada satu atau lebih kata dari keyword_list dalam preprocessed_comment
                    # if any(word in preprocessed_comment.split() for word in keyword_list):
                    original_comments.append(comment_text)
                    preprocessed_comments.append(preprocessed_comment)
                    if len(original_comments) >= 10:
                        break
                    # else:
                    #     continue

            try:
                # Tunggu hingga tombol 'load more' tersedia
                load_more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button._abl-")))
                load_more_button.click()
                time.sleep(2)  # Tambahkan delay agar elemen baru dapat dimuat
            except:
                break

        preprocessed_text["comments"] = preprocessed_comments[:10]
        original_text["comments"] = original_comments[:10]
    except Exception as e:
        print(f"Error while fetching comments: {e}")
    
    # Similarity
    cosine_similarity = similarity.calculateCosineSimilarity(preprocessed_text, keyword)
    asymetric_similarity = similarity.calculateAsymmetricSimilarity(preprocessed_text, keyword)

    # Bandingkan caption dan komentar terbaik
    display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity)

# Send json
json_output = json.dumps(results, ensure_ascii=False, indent=4)
print(json_output)

# Quit WebDriver
wd.quit()
