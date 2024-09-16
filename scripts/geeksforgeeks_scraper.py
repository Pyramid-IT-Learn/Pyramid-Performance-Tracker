# scripts/geeksforgeeks_scraper.py

import json
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from cmrit_leaderboard.config import GFG_WEEKLY_CONTEST_URL, GFG_PRACTICE_URL, GFG_API_URL, GEEKSFORGEEKS_URL, GFG_USERNAME, GFG_PASSWORD, DEBUG
import time

def scrape_geeksforgeeks_weekly_contest(users: pd.DataFrame) -> pd.DataFrame:
    # Create geeksforgeeksWeeklyRating column
    users['geeksforgeeksWeeklyRating'] = 0
    for _ in range(10000):
        print(f"Scraping GFG weekly contest page ${_}...")
        url = GFG_WEEKLY_CONTEST_URL + str(_)
        # Get json response
        response = requests.get(url)

        if response.status_code == 200:
            json_response = response.json()
        else:
            print(f"Error: {response.status_code}")
            exit(0)

        if json_response['results'] == []:
            break
        
        found_zero = False

        geeksforgeeks_user_set = set()
        # load users geeksforgeeks usernames into set
        for user in users['geeksforgeeksUsername']:
            geeksforgeeks_user_set.add(user.lower())

        for gfg_user in json_response['results']:
            gfg_response_username = str(gfg_user['user_handle']).lower()

            if gfg_response_username in geeksforgeeks_user_set:
                users.loc[users['geeksforgeeksUsername'] == str(gfg_user['user_handle']).lower(), 'geeksforgeeksWeeklyRating'] = gfg_user['user_score']
                print(f"Found user {gfg_user['user_handle'].lower()} with rating {gfg_user['user_score']}")
            if gfg_user['user_score'] == 0 or gfg_user['user_score'] == None:
                found_zero = True

        if found_zero:
            break

    return users

def scrape_geeksforgeeks_practice(users: pd.DataFrame) -> pd.DataFrame:
    # Create geeksforgeeksPracticeRating column
    users['geeksforgeeksPracticeRating'] = 0
    print("GFG practice scraping in progress...")
    
    # Initialize Firefox driver
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    
    # Log in to GeeksforGeeks
    print("Logging in to GeeksforGeeks...")
    driver.get("https://auth.geeksforgeeks.org/")
    try:
        username = driver.find_element(By.ID, "luser")
        password = driver.find_element(By.ID, "password")
        username.send_keys(GFG_USERNAME)
        password.send_keys(GFG_PASSWORD)
        driver.find_element(By.CLASS_NAME, "signin-button").click()
        print("Login successful.")
        time.sleep(5)  # Wait for the login process
    except Exception as e:
        print(f"Login error: {e}")
        driver.quit()
        return users

    # Scrape individual user profiles if practice rating is not available
    for index, user in users.iterrows():
        if not pd.isna(user['geeksforgeeksPracticeRating']):
            gfg_handle = user['geeksforgeeksUsername']
            driver.get(f"view-source:{GFG_API_URL}{gfg_handle}")
            time.sleep(0.1)
            
            try:
                # Parse JSON response
                try:
                    json_element = driver.find_element(By.TAG_NAME, "pre")
                    json_content = json.loads(json_element.text)
                except Exception as e:
                    raise RuntimeError(f"Error parsing JSON response for {user['hallTicketNo']} with LeetCode handle {gfg_handle}: {e}")
                
                try:
                    gfg_rating = json_content['data']['score']
                except Exception as e:
                    print(f"Error fetching practice rating for {gfg_handle}: {e.__class__.__name__} - {e}")
                    gfg_rating = 0

                if gfg_rating is None:
                    gfg_rating = 0

                users.at[index, 'geeksforgeeksPracticeRating'] = gfg_rating
                
                print(f"{index+1}/{len(users)} - Found practice rating for {user['hallTicketNo']} with GFG handle {gfg_handle}: {gfg_rating}")

            except (NoSuchElementException, ValueError) as e:
                print(f"Error fetching practice rating for {gfg_handle}: {e}")

    # Close the browser
    driver.quit()
    print("GFG practice scraping completed.")
    
    return users

def scrape_geeksforgeeks(users: pd.DataFrame) -> pd.DataFrame:
    users = scrape_geeksforgeeks_practice(users)  
    users = scrape_geeksforgeeks_weekly_contest(users)

    print("GFG scraping completed.")
    print(users[['hallTicketNo', 'geeksforgeeksUsername', 'geeksforgeeksWeeklyRating', 'geeksforgeeksPracticeRating']])

    return users