import json
import logging
import requests
import time
import random
from cmrit_leaderboard.config import CODECHEF_FILE, CODECHEF_LOG_FILE, CODECHEF_API_URL, CALL_INTERVAL, DEBUG
from .utils import setup_logger

codechef_logger = setup_logger("codechef_logger", CODECHEF_LOG_FILE, logging.DEBUG)

def check_codechef_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        response_json = response.json()
        # if success is true in the response json
        if response_json.get("success"):
            return True, response.url
        return False, response.url
    except requests.exceptions.RequestException as e:
        codechef_logger.error(f"Request failed: {e}")
    except json.decoder.JSONDecodeError:
        codechef_logger.error("Error decoding JSON response")
    except Exception as e:
        codechef_logger.error(f"Unexpected error: {e}")
    return False, url

def process_codechef(participants):
    last_request_time = time.time()
    total = len(participants)
    for index, participant in enumerate(participants, start=1):
        # Check CodeChef URL for each participant
        codechef_logger.debug(f"Checking CodeChef URL for participant ({index}/{total}) {participant.handle} with handle {participant.codechef_handle}")
        print(f"Checking CodeChef URL for participant ({index}/{total}) {participant.handle} with handle {participant.codechef_handle}")

        codechef_url_exists = False
        if "@" not in participant.codechef_handle and participant.codechef_handle != '':
            if participant.codechef_handle != '#n/a':
                current_time = time.time()
                time_since_last_request = current_time - last_request_time
                if time_since_last_request < CALL_INTERVAL:
                    wait_time = CALL_INTERVAL - time_since_last_request
                    wait_time += random.uniform(0, 2)  # Add some random jitter
                    print(f"Rate limit in effect. Waiting for {wait_time:.2f} seconds.")
                    codechef_logger.debug(f"Rate limit in effect. Waiting for {wait_time:.2f} seconds.")
                    time.sleep(wait_time)
                
                # Update the last request time
                last_request_time = time.time()

                # Check if CodeChef URL exists
                codechef_url_exists, response_url = check_codechef_url(
                    CODECHEF_API_URL + participant.codechef_handle)
                codechef_logger.debug(f"CodeChef URL exists: {codechef_url_exists}, Response URL: {response_url}")

            # Write participant data to file
            try:
                with open(CODECHEF_FILE, 'a') as file:
                    file.write(f"{participant.handle}, {participant.codechef_handle}, {codechef_url_exists}\n")
                codechef_logger.debug(f"Data written to file for participant {participant.handle}: {participant.codechef_handle},"
                            f" {codechef_url_exists}")
            except IOError as e:
                codechef_logger.error(f"Error writing to file: {e}")

        # Print progress and debug information
        print(f"Processed participant {index}/{len(participants)}: {participant.handle}")
        codechef_logger.debug(f"Processed participant {index}/{len(participants)}: {participant.handle}")

    codechef_logger.debug("CodeChef processing complete")
