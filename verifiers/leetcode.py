# verifiers/leetcode.py

import os
import time
import json
import urllib.parse
import undetected_chromedriver as uc
from ratelimiter import RateLimiter
from selenium.webdriver.common.by import By
from cmrit_leaderboard.config import LEETCODE_QUERY, MAX_REQUESTS_PER_SECOND, CHROME_DRIVER_VERSION, LEETCODE_FILE, DEBUG

def process_leetcode(participants):
    """
    Process the LeetCode handles of participants.

    :param participants: A list of Participant objects containing their handles and LeetCode handles.
    :return: None

    This function processes the LeetCode handles of participants by making API requests to retrieve their contest ranking information. It uses a rate limiter to ensure a maximum of 2 requests per second. The function uses undetected-chromedriver to run in headless mode and performs the following steps:
    1. Configures logging.
    2. Creates chrome options and configures undetected-chromedriver.
    3. Logs in to GitHub using the provided username and password.
    4. Opens a new tab and navigates to the LeetCode login page.
    5. Authorizes the GitHub login if prompted.
    6. Iterates over the participants and retrieves their contest ranking information using the LeetCode API.
    7. Parses the JSON response and checks if the response contains any errors.
    8. Writes the participant's handle, LeetCode handle, and a boolean indicating if the response was successful to a file.

    Note: The function assumes that the LeetCode API query is defined in the LEETCODE_QUERY variable and the maximum number of requests per second is defined in the MAX_REQUESTS_PER_SECOND variable.

    Raises:
    - RuntimeError: If there is an error parsing the JSON response or getting the content for a participant.
    - Exception: If there is an error processing the LeetCode handle for a participant.
    """
    # Configure logging
    counter = 1
    size = len(participants)

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
    username = os.environ.get('USERNAME')
    # load password from PASSWORD env variable
    passwd = os.environ.get('PASSWD')
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

    for participant in participants:
        handle = participant.handle
        leetcode_handle = participant.leetcode_handle
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

                try:
                    # Check if the response contains error
                    if json_content.get("errors"):
                        with open(LEETCODE_FILE, 'a') as file:
                            file.write(f"{handle}, {leetcode_handle}, False\n")
                        print(f"( {counter} / {size} ) Data written to file for participant {handle}: {leetcode_handle}, False")
                        print("---------------------------------------------------")
                        counter += 1
                        continue
                    else:
                        with open(LEETCODE_FILE, 'a') as file:
                            file.write(f"{handle}, {leetcode_handle}, True\n")
                        print(f"( {counter} / {size} ) Data written to file for participant {handle}: {leetcode_handle}, True")
                        print("---------------------------------------------------")
                        counter += 1
                except (KeyError, TypeError) as e:
                    raise RuntimeError(f"Error getting content for {handle} with LeetCode handle {leetcode_handle}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error processing LeetCode handle for {handle}: {e}")
