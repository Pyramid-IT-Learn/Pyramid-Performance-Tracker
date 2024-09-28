import time
import json
import requests
import pandas as pd

from cmrit_leaderboard.config import CODECHEF_API_URL, CALL_INTERVAL, CODECHEF_CLIENT_ID, CODECHEF_CLIENT_SECRET, DEBUG

def fetch_codechef_access_token():
    response = requests.post("https://api.codechef.com/oauth/token",
                         data={"grant_type": "client_credentials",
                               "scope": "public",
                               "client_id": f"{CODECHEF_CLIENT_ID}",
                               "client_secret": f"{CODECHEF_CLIENT_SECRET}",
                               "redirect_uri": ""})
    json_data = response.json()

    access_token = json_data["result"]["data"]["access_token"]

    return access_token

def fetch_codechef_score(username, access_token, depth=0):
    try:
        response = requests.get(f"{CODECHEF_API_URL}/users/{username}",
                                   headers={f"Authorization": f"Bearer {access_token}"},
                                   params={"fields": "ratings"},
                                   timeout=10)
        
        if response.status_code == 200:
            return response.json()["result"]["data"]["content"]["ratings"]["allContest"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            print("Trying again... Attempt: ", depth)
            if "Unauthorized" in response.text and depth < 100:
                return fetch_codechef_score(username, access_token, depth + 1)
            else:
                print("Too many recursive calls, exiting")
                exit(1)
    except KeyError:
        print("Invalid JSON response from Codechef API")
        print("--" * 30)
        print(response.text)
        print("--" * 30)
        return None
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codechef API")
        exit(1)

def scrape_codechef(users: pd.DataFrame) -> pd.DataFrame:
    last_request_time = time.time()
    total = len(users)
    
    access_token = fetch_codechef_access_token()
    token_fetch_time = time.time()  # Track when the token was fetched

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

                # Check if the token needs to be refreshed
                if current_time - token_fetch_time >= 3000:  # Token validity check (1 hour)
                    print("Access token expired. Fetching a new token...")
                    access_token = fetch_codechef_access_token()
                    token_fetch_time = time.time()  # Update the token fetch time
                
                print("Time since last token refresh:", time_since_last_request)
                print("Time left to create new token:", 3000 - (current_time - token_fetch_time))

                if time_since_last_request < CALL_INTERVAL:
                    wait_time = CALL_INTERVAL - time_since_last_request
                    print(f"Rate limit in effect. Waiting for {wait_time:.2f} seconds.")
                    time.sleep(wait_time)
                
                # Update the last request time
                last_request_time = time.time()

                # Get CodeChef score
                codechef_score = fetch_codechef_score(codechef_handle, access_token)

                if codechef_score is None:
                    codechef_score = 0

        # Update the DataFrame
        users.loc[index, 'codechefRating'] = codechef_score

        # Print progress
        print(f"Processed participant {index+1}/{len(users)}")
        print("--" * 10)

    return users
