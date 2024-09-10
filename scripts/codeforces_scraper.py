# scripts/codeforces_scraper.py

import time
import json
import requests
import pandas as pd

from cmrit_leaderboard.config import CODEFORCES_URL, API_KEY, API_SECRET, CODEFORCES_FILE, DEBUG
from verifiers.utils import generate_random_string, generate_api_sig

def fetch_codeforces_scores(handles):
    random_string = generate_random_string(6)
    current_time = int(time.time())
    handles_string = ';'.join([handle for handle in handles if handle != '#n/a'])
    api_sig = generate_api_sig(random_string, "user.info", handles_string, current_time, API_SECRET, API_KEY)
    # Construct the request URL
    url = f"{CODEFORCES_URL}/user.info?handles={handles_string}&apiKey={API_KEY}&time={current_time}&apiSig={random_string}{api_sig}"

    if DEBUG:
        print(f"Url: {url}")

    try:
        response = requests.get(url)
        json_response = response.json()
        return json_response
    except requests.RequestException as e:
        print(f"Error fetching Codeforces data: {e}")
        raise Exception("Failed to fetch Codeforces data.")
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codeforces API")
        print(response.text)
        raise Exception("Invalid JSON response from Codeforces API")

def scrape_codeforces(users: pd.DataFrame) -> pd.DataFrame:
    print("Starting Codeforces processing")

    # Load Codeforces handles from users df
    handles = {user["codeforcesUsername"] for index, user in users.iterrows() if user["codeforcesUsername"] != '#n/a' and "@" not in user["codeforcesUsername"]}
    
    # Create a list of sets of handles with max 300 elements in each set by popping elements from the handles
    batches = []
    temp_handles = set()
    while handles:
        temp_handles.add(handles.pop())
        if len(temp_handles) == 300:
            batches.append(temp_handles)
            temp_handles = set()
    if temp_handles:
        batches.append(temp_handles)

    for index, batch in enumerate(batches):
        current_batch_message = f"""
        =================================
        Processing batch {index + 1} of {len(batches)}
        =================================
        """

        print(current_batch_message)

        while True:
            response = fetch_codeforces_scores(batch)

            if response["status"] == "OK":
                for user in response["result"]:
                    rating = 0
                    try:
                        rating = user["rating"]
                    except KeyError:
                        print(f"KeyError: {user['handle']}")
                    except json.decoder.JSONDecodeError:
                        print(f"JSON error: {user['handle']}")

                    users.loc[users["codeforcesUsername"] == user["handle"].lower(), "codeforcesRating"] = rating

                break
            else:
                print(f"API Error: {response.get('comment', 'Unknown error')}")
                break

    print("Codeforces processing completed")

    return users


