import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import preprocessing  # Import preprocessing module for preprocessing

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

# Login details
username = "dummy_x_iir"  # Replace with your username
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
x_links = []

try:
    wd.get(f"https://x.com/search?q={keyword}&f=media")
    if not is_logged_in():
        perform_login()
        wd.get(f"https://x.com/search?q={keyword}&f=media")

    while len(x_links) < 10:
        time.sleep(3)
        try:
            x_results = wd.find_elements(By.CSS_SELECTOR, 'li.css-175oi2r a')
            for result in x_results:
                link = result.get_attribute('href')
                if "/photo/" in link and link not in x_links:
                    x_links.append(link)
                    if len(x_links) >= 10:
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
def display_results(source, original_text, preprocessed_text, similarity=0):
    print(f"Source: {source}")
    print("")
    print(f"Original text: {original_text}")
    print("")
    print(f"Preprocessed text: {preprocessed_text}")
    print("")
    print(f"Similarity: {similarity:.4f}")
    print("-" * 60)

# Process each post link
for idx, link in enumerate(x_links):
    wd.get(link)
    time.sleep(2)

    # Get Account name (nti diganti jadi x, instgram, atau youtube)
    try:
        account = WebDriverWait(wd, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='User-Name']"))).text
    except:
        account = "Account not available"

    # Get description 
    try:
        description = wd.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']").text
        preprocessed_description = preprocessing.stemmer_and_remove_stopwords(
            preprocessing.remove_prepocessing(description)
        )
    except:
        description = "No description available"
        preprocessed_description = ""

    best_comment = "No comment available"
    preprocessed_best_comment = ""

    # Get comment
    try:
        div_elements = wd.find_elements(By.CSS_SELECTOR, "[data-testid='cellInnerDiv']")
        for div in div_elements:
            try:
                comment = div.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']").text
                preprocessed_comment = preprocessing.stemmer_and_remove_stopwords(
                    preprocessing.remove_prepocessing(comment)
                )
                best_comment = comment
                preprocessed_best_comment = preprocessed_comment
            except:
                pass
    except:
        pass

    display_results(account, description, preprocessed_description, similarity=0)

wd.quit()
