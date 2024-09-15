# scripts/geeksforgeeks_scraper.py

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

"""
# Scrape GeeksforGeeks practice ratings: The long and tedious process is done here. #

def scrape_geeksforgeeks_practice(users: pd.DataFrame) -> pd.DataFrame:
    # Create geeksforgeeksPracticeRating column
    users['geeksforgeeksPracticeRating'] = 0
    print("GFG practice scraping in progress...")
    
    # Initialize counter
    counter = 1
    
    # Initialize Firefox driver
    options = Options()
    options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    
    # Log in to GeeksforGeeks
    driver.get("https://auth.geeksforgeeks.org/")
    try:
        username = driver.find_element(By.ID, "luser")
        password = driver.find_element(By.ID, "password")
        username.send_keys(GFG_USERNAME)
        password.send_keys(GFG_PASSWORD)
        driver.find_element(By.CLASS_NAME, "signin-button").click()
        time.sleep(5)  # Wait for the login process
    except Exception as e:
        print(f"Login error: {e}")
        driver.quit()
        return users

    # Overall Practice score scraping
    for j in range(1, 2):  # Just a single page as per Java example
        try:
            url = f"{GFG_PRACTICE_URL}{j}"
            print(f"Page: {j}")
            
            # Check if URL exists
            response = requests.get(url)
            if response.status_code in [404, 400]:
                break
            
            json_response = response.json()
            found_zero = False

            # Access parsed data and update user ratings
            for gfg_user in json_response['results']:
                gfg_handle = gfg_user['handle']
                user_row = users[users['geeksforgeeksUsername'] == gfg_handle]
                if not user_row.empty:
                    user_index = user_row.index[0]
                    users.at[user_index, 'geeksforgeeksPracticeRating'] = gfg_user.get('coding_score', 0)
                    print(f"Found user {gfg_handle} with rating {gfg_user.get('coding_score', 0)}")

                    counter += 1
                
                if gfg_user.get('coding_score', 0) == 0:
                    found_zero = True
            
            if found_zero:
                break
            
        except Exception as e:
            print(f"Error fetching GFG Practice rating: {e}")
    
    # Scrape individual user profiles if practice rating is not available
    for index, user in users.iterrows():
        if pd.isna(user['geeksforgeeksPracticeRating']):
            gfg_handle = user['geeksforgeeksUsername']
            print(f"Practice rating not found for {user['hallTicketNo']} with GFG handle {gfg_handle}. Fetching from profile...")
            driver.get(f"{GEEKSFORGEEKS_URL}{gfg_handle}")
            time.sleep(2)
            
            try:
                score_card_value = driver.find_element(By.XPATH, "//span[contains(text(), 'Overall Coding Score')]/following-sibling::br/following-sibling::span")
                gfg_rating = int(score_card_value.text)
                users.at[index, 'geeksforgeeksPracticeRating'] = gfg_rating
                
                print(f"Found practice rating for {user['handle']} with GFG handle {gfg_handle}: {gfg_rating}")

                counter += 1
            except (NoSuchElementException, ValueError) as e:
                print(f"Error fetching practice rating for {gfg_handle}: {e}")

    # Close the browser
    driver.quit()
    print("GFG practice scraping completed.")
    
    return users

"""

def scrape_geeksforgeeks_practice_api(users: pd.DataFrame) -> pd.DataFrame:
    # Create geeksforgeeksPracticeRating column
    users['geeksforgeeksPracticeRating'] = 0
    print("GFG practice scraping in progress...")

    # Initialize counter
    counter = 1

    for index, user in users.iterrows():
        gfg_handle = user['geeksforgeeksUsername']
        print(f"Practice rating not found for {user['hallTicketNo']} with GFG handle {gfg_handle}. Fetching from profile...")

        try:
            response = requests.get(f"{GEEKSFORGEEKS_URL}{gfg_handle}")
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get('message') == 'User not found!':
                    continue
                if json_response.get('data', {}).get('score') is not None:
                    gfg_rating = json_response['data']['score']
                users.at[index, 'geeksforgeeksPracticeRating'] = gfg_rating
                print(f"Found practice rating for {index}/{len(users)} {user['handle']} with GFG handle {gfg_handle}: {gfg_rating}")
        except Exception as e:
            print(f"Error fetching practice rating for {gfg_handle}: {e}")

def scrape_geeksforgeeks(users: pd.DataFrame) -> pd.DataFrame:
    users = scrape_geeksforgeeks_weekly_contest(users)
    users = scrape_geeksforgeeks_practice_api(users)

    print("GFG scraping completed.")
    print(users[['hallTicketNo', 'geeksforgeeksUsername', 'geeksforgeeksWeeklyRating', 'geeksforgeeksPracticeRating']])

    return users