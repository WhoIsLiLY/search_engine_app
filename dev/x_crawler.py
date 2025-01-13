import sys
import json
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import preprocessing  # Import preprocessing module for preprocessing
import similarity

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode if desired
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Initialize WebDriver with options
wd = webdriver.Chrome(options=chrome_options)

# List of Dictionaries to save the result
results = []

# Login details
# username = "dummy_x_iir"  # Replace with your username
username = "XDummy47097"
password = "dummytwitter"  # Replace with your password

def perform_login():
    # Step 1: Go to the login page
    wd.get("https://x.com/i/flow/login")

    # Step 2: Enter username and click "Next"
    WebDriverWait(wd, 100).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    wd.find_element(By.NAME, "text").send_keys(username)
    # print("Entered username")

    # Find and click the "Next" button after entering the username
    try:
        next_button = WebDriverWait(wd, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Next')]"))
        )
        next_button.click()
        # print("Clicked 'Next' button")
    except Exception as e:
        print(f"Failed to click 'Next' button: {e}")

    # Step 3: Enter password
    WebDriverWait(wd, 100).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    wd.find_element(By.NAME, "password").send_keys(password)
    # print("Entered password")

    # Step 4: Click the "Log in" button
    try:
        login_button = WebDriverWait(wd, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in')]"))
        )
        login_button.click()
        # print("Clicked 'Log in' button")
    except Exception as e:
        print(f"Failed to click 'Log in' button: {e}")

    # Step 5: Confirm successful login by checking URL or page content
    try:
        WebDriverWait(wd, 100).until(
            EC.url_changes("https://x.com/i/flow/login")
        )
        # print("Login successful")
    except Exception as e:  
        print(f"Failed to log in: {e}")

perform_login()

def is_logged_in():
    return "login" not in wd.current_url


# Continue with the crawling logic

keyword = " ".join(sys.argv[1:])
keyword = preprocessing.stemmer_and_remove_stopwords(
          preprocessing.preprocess_text(keyword)
        )

# keyword = "ppn 12"
x_links = []

try:
    wd.get(f"https://x.com/search?q={keyword}&f=media")
    if not is_logged_in():
        perform_login()
        wd.get(f"https://x.com/search?q={keyword}&f=media")

    while len(x_links) < 2:
        time.sleep(3)
        try:
            x_results = wd.find_elements(By.CSS_SELECTOR, 'li.css-175oi2r a')
            for result in x_results:
                link = result.get_attribute('href')
                if "/photo/" in link and link not in x_links:
                    x_links.append(link)
                    if len(x_links) >= 2:
                        break
        except Exception as e:
            print(f"Failed to fetch X search results: {e}")
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if not x_links:
        print("No posts found.")
        wd.quit()
        sys.exit(1)

# Display Result
def display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity):
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

def wait_for_element(driver, selector, timeout=10):
    """Helper function to wait for element and handle exceptions"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return element
    except TimeoutException:
        return None

# Process each post link
for idx, link in enumerate(x_links):
    wd.get(link)
    
    original_text = {
        "caption": "",
        "comments": []
    }
    preprocessed_text = {
        "caption": "",
        "comments": []
    }

    # Get caption - wait for tweet text to be present
    try:
        caption_element = wait_for_element(wd, "[data-testid='tweetText']")
        if caption_element:
            original_caption = " " + caption_element.text
            preprocessed_caption = preprocessing.stemmer_and_remove_stopwords(
                preprocessing.preprocess_text(original_caption)
            )
        else:
            original_caption = ""
            preprocessed_caption = ""
    except:
        original_caption = ""
        preprocessed_caption = ""
    
    original_text["caption"] = original_caption
    preprocessed_text["caption"] = preprocessed_caption
    
    # Get comments - wait for comments container
    try:
        # Wait for comments to load
        comments_loaded = wait_for_element(wd, "[data-testid='cellInnerDiv']")
        if comments_loaded:
            # Use explicit wait with multiple attempts for handling dynamic loading
            for attempt in range(3):  # Try up to 3 times
                try:
                    div_elements = WebDriverWait(wd, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='cellInnerDiv']"))
                    )
                    
                    for div in div_elements[1:]:
                        try:
                            # Wait for each comment text to be loaded
                            comment_element = WebDriverWait(div, 3).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='tweetText']"))
                            )
                            comment = comment_element.text
                            preprocessed_comments = preprocessing.stemmer_and_remove_stopwords(
                                preprocessing.preprocess_text(comment)
                            )
                            original_text["comments"].append(comment)
                            preprocessed_text["comments"].append(preprocessed_comments)
                        except (TimeoutException, StaleElementReferenceException):
                            continue
                    break  # If successful, break the retry loop
                except (TimeoutException, StaleElementReferenceException):
                    if attempt == 2:  # Last attempt
                        print(f"Failed to load comments after {attempt + 1} attempts")
    except Exception as e:
        print(f"Error loading comments: {str(e)}")
    
    # Calculate Similarity
    cosine_similarity = similarity.calculateCosineSimilarity(preprocessed_text, keyword)
    asymetric_similarity = similarity.calculateAsymmetricSimilarity(preprocessed_text, keyword)

    display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity)

# Send json
json_output = json.dumps(results, ensure_ascii=False, indent=4)
print(json_output)
wd.quit()
