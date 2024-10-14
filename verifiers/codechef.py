import json
import requests
import time
import random
from cmrit_leaderboard.config import CODECHEF_FILE, CODECHEF_API_URL, CALL_INTERVAL, CODECHEF_CLIENT_ID, CODECHEF_CLIENT_SECRET, DEBUG


def fetch_codechef_access_token():
    try:
        response = requests.post("https://api.codechef.com/oauth/token",
                             data={"grant_type": "client_credentials",
                                   "scope": "public",
                                   "client_id": f"{CODECHEF_CLIENT_ID}",
                                   "client_secret": f"{CODECHEF_CLIENT_SECRET}",
                                   "redirect_uri": ""})
        json_data = response.json()

        print(json.dumps(json_data, indent=2))

        access_token = json_data["result"]["data"]["access_token"]

        return access_token
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codechef API")
        print("--" * 30)
        print(response.text)
        print("--" * 30)
        exit(1)

#
# Multiple users URL tester, old, will be replaced
#
# def check_codechef_url(username, access_token):
#     try:
#         response = requests.get(f"{CODECHEF_API_URL}/users",
#                                    headers={f"Authorization": f"Bearer {access_token}"},
#                                    params={"fields": ['fullname'],
#                                            "search": f'{username}'},
#                                    timeout=10)
#         
#         if response.status_code == 200:
#             if "message" in response.json()["result"]["data"] and (response.json()["result"]["data"]["message"] == "user does not exists" or response.json()["result"]["data"]["message"] == "no user found for this search"):
#                 return False
#             else:
#                 for user in response.json()["result"]["data"]["content"]:
#                     if user["username"] == username:
#                         return True
#             return False
#         else:
#             print(f"Error: {response.status_code} - {response.text}")
#             exit(1)
#         
#     except json.decoder.JSONDecodeError:
#         print("Invalid JSON response from Codechef API")
#         print("--" * 30)
#         print(response.text)
#         print("--" * 30)
#         exit(1)

def check_codechef_url(username, access_token):
    try:
        response = requests.get(f"{CODECHEF_API_URL}/users/{username}",
                                   headers={f"Authorization": f"Bearer {access_token}"},
                                   params={"fields": "ratings"},
                                   timeout=10)
        # Print response as json
        print(json.dumps(response.json(), indent=2))
        if response.status_code == 200:
            if "message" in response.json()["result"]["data"] and (response.json()["result"]["data"]["message"] == "user does not exists" or response.json()["result"]["data"]["message"] == "no user found for this search"):
                return False
            else:
                return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            exit(1)
        
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codechef API")
        print("--" * 30)
        print(response.text)
        print("--" * 30)
        exit(1)

def process_codechef(participants):
    access_token = fetch_codechef_access_token()
    token_fetch_time = time.time()  # Track when the token was fetched
    last_request_time = time.time()
    total = len(participants)
    
    for index, participant in enumerate(participants, start=1):
        # Check CodeChef URL for each participant
        print(f"Checking CodeChef URL for participant ({index}/{total}) {participant.handle} with handle {participant.codechef_handle}")

        codechef_url_exists = False
        if "@" not in participant.codechef_handle and participant.codechef_handle != '':
            if participant.codechef_handle != '#n/a':
                current_time = time.time()
                time_since_last_request = current_time - last_request_time

                # Check if the token needs to be refreshed
                if current_time - token_fetch_time >= 3000:  # Token validity check (1 hour)
                    print("Access token expired. Fetching a new token...")
                    access_token = fetch_codechef_access_token()
                    token_fetch_time = time.time()  # Update the token fetch time
                
                if time_since_last_request < CALL_INTERVAL:
                    wait_time = CALL_INTERVAL - time_since_last_request
                    wait_time += random.uniform(0, 2)  # Add some random jitter
                    print(f"Rate limit in effect. Waiting for {wait_time:.2f} seconds.")
                    time.sleep(wait_time)
                
                # Update the last request time
                last_request_time = time.time()

                # Check if CodeChef URL exists
                codechef_url_exists = check_codechef_url(participant.codechef_handle, access_token)
                print(f"CodeChef URL exists: {codechef_url_exists}")

            # Write participant data to file
            try:
                with open(CODECHEF_FILE, 'a') as file:
                    file.write(f"{participant.handle}, {participant.codechef_handle}, {codechef_url_exists}\n")

            except IOError as e:
                print(f"Error writing to file: {e}")

        # Print progress and debug information
        print(f"Processed participant {index}/{len(participants)}: {participant.handle}")

    print("CodeChef processing complete")
