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

# Handle encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Validate keyword argument
if len(sys.argv) < 2:
    print("Error: Keyword argument is missing. Usage: python instagram_crawler.py <keyword>")
    sys.exit(1)

# List of Dictionaries to save the result
results = []

# Combine all keyword arguments into a single string
keyword = " ".join(sys.argv[1:])
keyword = preprocessing.stemmer_and_remove_stopwords(
          preprocessing.remove_prepocessing(keyword)
        )

# Setup Selenium Chrome options
chrome_options = Options()
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

# Instagram login
username = "dummy_ig_iir"  # Replace with your Instagram username
password = "dummyinstagram"  # Replace with your Instagram password

try:
    wd.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(wd, 30).until(EC.presence_of_element_located((By.NAME, "username")))

    wd.find_element(By.NAME, "username").send_keys(username)
    wd.find_element(By.NAME, "password").send_keys(password)

    login_button = WebDriverWait(wd, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in') or contains(., 'Masuk')]"))
    )
    login_button.click()

    WebDriverWait(wd, 30).until(EC.url_changes("https://www.instagram.com/accounts/login/"))
except Exception as e:
    print(f"Failed to log in: {e}")
    wd.quit()
    sys.exit(1)

# Search Instagram posts on Google
query = "site:instagram.com+inurl:/p/+" + keyword
google_links = []
seen_links = set()
start = 0

while len(google_links) < 10:
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
                if len(google_links) >= 10:
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
def display_results(original_text, preprocessed_text, similarity=0):
    result = {
        "Source": "Instagram",
        "Original Text": original_text,
        "Preprocessed Text": preprocessed_text,
        "Similarity": similarity
    }
    results.append(result)
    # print(f"Original Text: {original_text}")
    # print("")
    # print(f"Preprocessed Text: {preprocessed_text}")
    # print("")
    # print(f"Similarity: {similarity:.4f}")
    # print("-" * 60)


for idx, link in enumerate(google_links):
    wd.get(link)
    time.sleep(2)

    original_text = ""
    preprocessed_text = ""
 
    # Get account name
    try:
        account = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.x1vvkbs"))
        ).text
    except:
        account = "Account not available"

    # Get caption
    try:
        original_text += " " + wd.find_element(By.CSS_SELECTOR, "h1._aade").text
        # preprocessed_caption = preprocessing.stemmer_and_remove_stopwords(
        #     preprocessing.remove_prepocessing(caption)
        # )
    except:
        caption = "No caption available"

    # Get comments
    try:
        comments = wd.find_elements(By.CSS_SELECTOR, "ul._a9ym li span._aaco")
        for comment in comments:
            try:
                original_text += " " + comment.text  # Ambil teks komentar
            except:
                pass
    except:
        pass
    
    preprocessed_text = preprocessing.stemmer_and_remove_stopwords(
            preprocessing.remove_prepocessing(original_text)
        )
    
    # Similarity
    similarity = 0 # Panggil function perhitungan similaritas disini

    # Bandingkan caption dan komentar terbaik
    display_results(original_text, preprocessed_text, similarity)

# Send json
json_output = json.dumps(results, ensure_ascii=False, indent=4)
print(json_output)

# Quit WebDriver
wd.quit()
