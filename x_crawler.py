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
# chrome_options.add_argument("--headless")  # Run in headless mode if desired
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
    
# Get comments - wait for comments container
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
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
            original_caption = caption_element.text
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
    
    # get comments
    try:
        original_comments = []
        preprocessed_comments = []
        wait = WebDriverWait(wd, 10)
        max_attempts = 10
        attempt = 0

        while len(original_comments) < 10 and attempt < max_attempts:
            attempt += 1
            try:
                scroll_to_bottom(wd)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='cellInnerDiv']")))
                div_elements = wd.find_elements(By.CSS_SELECTOR, "[data-testid='cellInnerDiv']")
                # print(f"Found {len(div_elements)} elements")

                for div in div_elements:
                    try:
                        comment_text = div.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']").text
                        # print(f"Processing comment: {comment_text[:50]}...")
                        
                        if comment_text not in original_comments:
                            keyword_list = keyword.split()
                            preprocessed_comment = preprocessing.stemmer_and_remove_stopwords(
                                preprocessing.preprocess_text(comment_text)
                            )
                            
                            # if any(word in preprocessed_comment.split() for word in keyword_list):
                            original_comments.append(comment_text)
                            preprocessed_comments.append(preprocessed_comment)
                            # print(f"Added comment. Total comments: {len(original_comments)}")
                            if len(original_comments) >= 10:
                                break
                    except Exception as e:
                        print("") #"Error processing element: {e}"
                        continue

            except Exception as e:
                print("") #"Error in main loop: {e}"
                time.sleep(2)  # Wait before retrying

        preprocessed_text["comments"] = preprocessed_comments[:10]
        original_text["comments"] = original_comments[:10]
        
        # print(f"Final number of comments collected: {len(original_comments)}")
        
    except Exception as e:
        print("") #"Error while fetching comments: {e}"

    # Similarity
    cosine_similarity = similarity.calculateCosineSimilarity(preprocessed_text, keyword)
    asymetric_similarity = similarity.calculateAsymmetricSimilarity(preprocessed_text, keyword)

    # Bandingkan caption dan komentar terbaik
    display_results(original_text, preprocessed_text, cosine_similarity, asymetric_similarity)

# Send json
json_output = json.dumps(results, ensure_ascii=False, indent=4)
print(json_output)
wd.quit()
