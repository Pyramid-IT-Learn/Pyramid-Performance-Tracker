# scripts/leetcode_scraper.py

import time
import json
import urllib.parse
import pandas as pd
import undetected_chromedriver as uc
from ratelimiter import RateLimiter
from selenium.webdriver.common.by import By
from cmrit_leaderboard.config import LEETCODE_QUERY, MAX_REQUESTS_PER_SECOND, CHROME_DRIVER_VERSION, LEETCODE_FILE, GIT_USERNAME, GIT_PASSWORD, DEBUG

def scrape_leetcode(users: pd.DataFrame) -> pd.DataFrame:
    # Create a new column to store the LeetCode ratings
    users['leetcodeRating'] = 0
    # Configure logging
    counter = 1
    size = len(users)

    # Rate limit the function to a maximum of 2 requests per second
    limiter = RateLimiter(max_calls=MAX_REQUESTS_PER_SECOND, period=1)

    # Create chrome options
    options = uc.ChromeOptions()
    options.add_argument("--auto-open-devtools-for-tabs")

    # Configure undetected-chromedriver to run in headless mode
    driver = uc.Chrome(version_main=CHROME_DRIVER_VERSION, options=options)

    # Login to GitHub
    driver.get("https://github.com/login")
    time.sleep(5)
    login = driver.find_element(By.NAME, "login")
    password = driver.find_element(By.NAME, "password")
    signin_btn = driver.find_element(By.NAME, "commit")
    # load username from USERNAME env variable
    username = GIT_USERNAME
    # load password from PASSWORD env variable
    passwd = GIT_PASSWORD
    login.send_keys(username)
    password.send_keys(passwd)
    signin_btn.click()

    # Open new tab to https://leetcode.com/accounts/login/
    driver.get('https://leetcode.com/accounts/github/login/?next=%2F')
    time.sleep(5)
    try:
        authorize_btn = driver.find_element(By.NAME, "authorize")
        authorize_btn.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")

    for index, participant in users.iterrows():
        handle = participant['hallTicketNo']
        leetcode_handle = participant['leetcodeUsername']
        # Construct URL for API request
        encoded_leetcode_handle = urllib.parse.quote(leetcode_handle, safe='')
        url = LEETCODE_QUERY.replace("{<username>}", encoded_leetcode_handle)
        url = url.replace(" ", "%20")
        try:
            with limiter:
                driver.get(url)

                # Parse JSON response
                try:
                    json_content = driver.find_element(By.TAG_NAME, "pre").text
                    json_content = json.loads(json_content)
                except Exception as e:
                    raise RuntimeError(f"Error parsing JSON response for {handle} with LeetCode handle {leetcode_handle}: {e}")
                
                if json_content['data']['userContestRanking']:
                    users.at[index, 'leetcodeRating'] = json_content["data"]["userContestRanking"]["rating"]
                    print(f"Found user {handle} with rating {json_content['data']['userContestRanking']['rating']}")

                else:
                    print(f"No rating found for user {handle} with LeetCode handle {leetcode_handle}")

        except Exception as e:
            raise RuntimeError(f"Error processing LeetCode handle for {handle}: {e}")
        
    print("LeetCode scraping completed.")
    print(users[['hallTicketNo', 'leetcodeUsername', 'leetcodeRating']])

    return users
