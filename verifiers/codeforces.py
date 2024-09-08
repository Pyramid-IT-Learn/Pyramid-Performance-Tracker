# verifiers/codeforces.py

import logging
import requests
import time
import re
from cmrit_leaderboard.config import CODEFORCES_URL, API_KEY, API_SECRET, CODEFORCES_FILE, CODEFORCES_LOG_FILE, DEBUG
from .utils import generate_random_string, generate_api_sig, setup_logger

codeforces_logger = setup_logger('codeforces', CODEFORCES_LOG_FILE, DEBUG)

def check_codeforces_users(handles):
    random_string = generate_random_string(6)
    current_time = int(time.time())
    handles_string = ';'.join([handle for handle in handles if handle != '#n/a'])
    api_sig = generate_api_sig(random_string, "user.info", handles_string, current_time, API_SECRET, API_KEY)
    # Construct the request URL
    url = f"{CODEFORCES_URL}/user.info?handles={handles_string}&apiKey={API_KEY}&time={current_time}&apiSig={random_string}{api_sig}"

    if DEBUG:
        codeforces_logger.debug(f"Url: {url}")

    try:
        response = requests.get(url)
        json_response = response.json()
        codeforces_logger.debug(f"Response from Codeforces API: {json_response}")
        return json_response
    except requests.RequestException as e:
        codeforces_logger.error(f"Error fetching Codeforces data: {e}")
        raise Exception("Failed to fetch Codeforces data.")

def process_codeforces(participants):
    codeforces_logger.debug("Starting Codeforces processing")

    # Load Codeforces handles from participants
    handles = {participant.codeforces_handle.replace(" ", "") for participant in participants if participant.codeforces_handle != '#n/a' and "@" not in participant.codeforces_handle}

    final_valid_handles = set()
    final_invalid_handles = set()
    
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

        codeforces_logger.debug(f"Processing batch {index + 1} of {len(batches)}")

        while True:
            response = check_codeforces_users(batch)

            if response["status"] == "OK":
                # Add all valid handles to final_valid_handles
                final_valid_handles = final_valid_handles.union(batch)

                codeforces_logger.debug(f"Valid handles: {final_valid_handles}")
                codeforces_logger.debug(f"Invalid handles: {final_invalid_handles}")

                break

            elif response["status"] == "FAILED" and response["comment"].startswith("handles:"):
                # Read result and add all invalid handles to final_invalid_handles
                handles_to_remove = {re.search(r"User with handle (.+) not found", response["comment"]).group(1).lower()}
                print(f"Handles to remove: {handles_to_remove}")
                codeforces_logger.debug(f"Handles to remove: {handles_to_remove}")
                final_valid_handles = final_valid_handles - handles_to_remove
                final_invalid_handles = final_invalid_handles.union(handles_to_remove)
                batch = batch - handles_to_remove

            else:
                codeforces_logger.error(f"API Error: {response.get('comment', 'Unknown error')}")
                break

    # Write the report to a file
    with open(CODEFORCES_FILE, 'w') as f:
        for participant in participants:
            if participant.codeforces_handle:
                if participant.codeforces_handle in final_valid_handles:
                    f.write(f"{participant.handle}, {participant.codeforces_handle}, {True}\n")
                else:
                    f.write(f"{participant.handle}, {participant.codeforces_handle}, {False}\n")

    codeforces_logger.debug(f"Data written to file for batch {index + 1} of {len(batches)}")

    codeforces_logger.debug("Codeforces processing completed")

