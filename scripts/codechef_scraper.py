# scripts/codechef_scraper.py

import time
import json
import requests
import pandas as pd

from cmrit_leaderboard.config import CODECHEF_API_URL, CALL_INTERVAL, DEBUG

def fetch_codechef_score(url):
    try:
        response = requests.get(url)
        response_json = response.json()
        # if success is true in the response json
        if response_json.get("success"):
            return True, response
        return False, response
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codechef API")
        exit(0)

def scrape_codechef(users: pd.DataFrame) -> pd.DataFrame: 
    last_request_time = time.time()
    total = len(users)

    for index, user in users.iterrows():
        print("--" * 10)
        hallTicketNo = user['hallTicketNo']
        codechef_handle = user['codechefUsername']
        codechef_score = 0

        print(f"\nProcessing participant ({index+1}/{total}): {hallTicketNo} with handle {codechef_handle}")

        if "@" not in codechef_handle and codechef_handle != '':
            if codechef_handle != '#n/a':
                current_time = time.time()
                time_since_last_request = current_time - last_request_time
                if time_since_last_request < CALL_INTERVAL:
                    wait_time = CALL_INTERVAL - time_since_last_request
                    print(f"Rate limit in effect. Waiting for {wait_time:.2f} seconds.")
                    time.sleep(wait_time)
                
                # Update the last request time
                last_request_time = time.time()

                # Check if CodeChef URL exists
                codechef_url_exists, response = fetch_codechef_score(
                    CODECHEF_API_URL + codechef_handle)
                print(f"CodeChef URL exists: {codechef_url_exists}, Response: {response.text}")

                rating = 0
                try:
                    temp = response.json().get("currentRating")
                    if temp is not None:
                        rating = temp
                except json.decoder.JSONDecodeError:
                    print("Invalid JSON response from Codechef API")

                # Write participant data to file
                codechef_score = rating

        # Update the DataFrame
        users.loc[index, 'codechefRating'] = codechef_score

        # Print progress
        print(f"Processed participant {index+1}/{len(users)}")
        print("--" * 10)

    return users

