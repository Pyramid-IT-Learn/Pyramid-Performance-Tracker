# verifiers/codeforces.py

import logging
import requests
import time
import re
from cmrit_leaderboard.config import CODEFORCES_URL, API_KEY, API_SECRET, CODEFORCES_FILE, DEBUG
from .utils import generate_random_string, generate_api_sig

def check_codeforces_users(handles):
    random_string = generate_random_string(6)
    current_time = int(time.time())
    handles_string = ';'.join(handles)
    api_sig = generate_api_sig(random_string, "user.info", handles_string, current_time, API_SECRET, API_KEY)
    # Construct the request URL
    url = f"{CODEFORCES_URL}/user.info?handles={handles_string}&apiKey={API_KEY}&time={current_time}&apiSig={random_string}{api_sig}"

    print("===========================")
    print("Url: ", url)
    print("===========================")

    try:
        response = requests.get(url)
        json_response = response.json()
        if DEBUG:
            logging.debug(f"Response from Codeforces API: {json_response}")
        return json_response
    except requests.RequestException as e:
        logging.error(f"Error fetching Codeforces data: {e}")
        raise Exception("Failed to fetch Codeforces data.")

def process_codeforces(participants):
    logging.basicConfig(filename='codeforces_debug.log', level=logging.DEBUG)
    handles = {participant.codeforces_handle.replace(" ", "") for participant in participants if participant.codeforces_handle and "@" not in participant.codeforces_handle}
    remaining_handles = set(handles)
    all_valid_handles = set()
    all_batches_successful = True

    batches = [list(remaining_handles)[i:i + 300] for i in range(0, len(remaining_handles), 300)]
    for index, batch in enumerate(batches, start=1):
        logging.info(f"Processing batch {index} of {len(batches)}")
        while True:
            response_json = check_codeforces_users(batch)
            if response_json["status"] == "OK":
                users = response_json["result"]
                valid_handles = {user["handle"] for user in users}
                all_valid_handles.update(valid_handles)
                handles_to_remove = set(batch) - valid_handles
                remaining_handles -= handles_to_remove
                if handles_to_remove:
                    logging.debug(f"Handles not found: {handles_to_remove}")
                break
            elif response_json["status"] == "FAILED" and response_json["comment"].startswith("handles:"):
                handles_to_remove = {re.search(r"User with handle (.+) not found", response_json["comment"]).group(1)}
                remaining_handles -= handles_to_remove
                batch.remove(handles_to_remove.pop())
                logging.warning(f"Handles not found: {handles_to_remove}")
            else:
                logging.error(f"API Error: {response_json.get('comment', 'Unknown error')}")
                all_batches_successful = False
                break
    with open(CODEFORCES_FILE, 'a') as file:
        for participant in participants:
            participant.codeforces_handle = participant.codeforces_handle.replace(" ", "")
            file.write(f"{participant.handle}, {participant.codeforces_handle}, {participant.codeforces_handle in all_valid_handles}\n")
    if all_batches_successful:
        logging.info("All batches processed successfully!")
    else:
        logging.error("Some batches failed to process.")
    logging.shutdown()
