# verifiers/geeksforgeeks.py

import logging
import requests
from cmrit_leaderboard.config import GEKSFORGEEKS_FILE, GEEKSFORGEEKS_LOG_FILE, DEBUG

def check_geekforgeeks_url(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }
    response = requests.get(url, headers=header)
    try:
        if response.status_code == 200:
            # Check if the final URL is the same as the original URL (no redirect), if redirected, then URL does not
            # exist codeforces redirect is found by checking if final url is https://codeforces.com/ geeksforgeeks
            # redirect is found by checking if final url is
            # https://auth.geeksforgeeks.org/?to=https://auth.geeksforgeeks.org/profile.php codechef redirect is
            # found by checking if final url is https://www.codechef.com/ Hackerrank and Leetcode return 404 error if
            # handle does not exist
            logging.debug(f"Checking : {response.url}")
            if (response.url == "https://auth.geeksforgeeks.org/?to=https://auth.geeksforgeeks.org/profile.php"):
                return False, response.url
            else:
                return True, response.url
        return False, response.url
    except requests.exceptions.RequestException:
        return False, "Exception"

def process_geeksforgeeks(participants):
    """
    Process GeeksForGeeks handles for each participant and log the progress.

    Args:
    participants (list): List of participant objects

    Returns:
    None
    """
    # Configure logging
    logging.basicConfig(filename=GEEKSFORGEEKS_LOG_FILE, level=logging.DEBUG)

    # Iterate through each participant
    total = len(participants)
    for i, participant in enumerate(participants, 1):
        geeksforgeeks_url_exists = False

        if participant.geeksforgeeks_handle != '#n/a':
            # Check if GeeksForGeeks handle is valid
            logging.debug(f"Checking GeeksForGeeks URL for participant {participant.handle}")

            # Check if the GeeksForGeeks URL exists
            geeksforgeeks_url_exists, response_url = check_geekforgeeks_url(
                "https://auth.geeksforgeeks.org/user/" + participant.geeksforgeeks_handle)
            logging.debug(f"GeeksForGeeks URL exists: {geeksforgeeks_url_exists}, Response URL: {response_url}")

            # Retry if the GeeksForGeeks URL does not exist
            if not geeksforgeeks_url_exists and participant.geeksforgeeks_handle != '#N/A':
                logging.debug(f"Retrying GeeksForGeeks URL check for participant {participant.handle}")
                geeksforgeeks_url_exists, response_url = check_geekforgeeks_url(
                    "https://auth.geeksforgeeks.org/user/" + participant.geeksforgeeks_handle)
                logging.debug(f"GeeksForGeeks URL retry: {geeksforgeeks_url_exists}, Response URL: {response_url}")

        # Write participant data to file
        with open(GEKSFORGEEKS_FILE, 'a') as file:
            file.write(f"{participant.handle}, {participant.geeksforgeeks_handle}, {geeksforgeeks_url_exists}\n")
        logging.debug(
            f"Data written to file for participant {participant.handle}: {participant.geeksforgeeks_handle},"
            f" {geeksforgeeks_url_exists}")
        logging.debug("---------------------------------------------------")

        print(f"{i}/{total}: {participant.handle} with handle {participant.geeksforgeeks_handle} result: {geeksforgeeks_url_exists}")

    logging.shutdown()