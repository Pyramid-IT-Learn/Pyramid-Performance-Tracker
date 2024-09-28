# verifiers/codeforces.py

import json
import requests
import time
import re
from cmrit_leaderboard.config import CODEFORCES_URL, API_KEY, API_SECRET, CODEFORCES_FILE, DEBUG
from .utils import generate_random_string, generate_api_sig


def check_codeforces_users(handles):
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
    except json.decoder.JSONDecodeError:
        print("Invalid JSON response from Codeforces API")
        print(url)
        print(response.text)
        # Try again, if response is still invalid raise exception
        time.sleep(5)
        response = requests.get(url)
        json_response = response.json()

        if json_response["status"] == "OK":
            return json_response
        
        raise Exception("Invalid JSON response from Codeforces API")
    except requests.RequestException as e:
        print(f"Error fetching Codeforces data: {e}")
        raise Exception("Failed to fetch Codeforces data.")

def process_codeforces(participants):
    # Load Codeforces handles from participants
    handles = {participant.codeforces_handle.replace(" ", "") for participant in participants if participant.codeforces_handle != '#n/a' and "@" not in participant.codeforces_handle}

    final_valid_handles = set()
    final_invalid_handles = set()

    # Create a list of sets of handles with max 300 elements in each set by popping elements from the handles
    batches = []
    temp_handles = set()
    while handles:
        temp_handles.add(handles.pop())
        if len(temp_handles) == 450:
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
            response = check_codeforces_users(batch)            

            if response["status"] == "OK":
                # Add all valid handles to final_valid_handles
                final_valid_handles = final_valid_handles.union(batch)

                break

            elif response["status"] == "FAILED" and response["comment"].startswith("handles:"):
                # Read result and add all invalid handles to final_invalid_handles
                handles_to_remove = {re.search(r"User with handle (.+) not found", response["comment"]).group(1).lower()}
                print(f"Handles to remove: {handles_to_remove}")
                final_valid_handles = final_valid_handles - handles_to_remove
                final_invalid_handles = final_invalid_handles.union(handles_to_remove)
                batch = batch - handles_to_remove

            else:
                print(f"Response: {response}")
                break
        

    # Write the report to a file
    with open(CODEFORCES_FILE, 'w') as f:
        for participant in participants:
            if participant.codeforces_handle:
                if participant.codeforces_handle in final_valid_handles:
                    f.write(f"{participant.handle}, {participant.codeforces_handle}, {True}\n")
                else:
                    f.write(f"{participant.handle}, {participant.codeforces_handle}, {False}\n")

    print(f"Total valid handles: {len(final_valid_handles)}")
    print(f"Total invalid handles: {len(final_invalid_handles)}")
