# verifiers/hackerrank.py

import logging
import requests
from cmrit_leaderboard.config import HACKERRANK_FILE, DEBUG
from time import sleep

def check_url_exists(url):
    try:
        response = requests.get(url)
        return response.status_code == 200, response.url
    except requests.RequestException as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False, None

def process_hackerrank(participants):
    logging.basicConfig(filename='hackerrank_debug.log', level=logging.DEBUG)
    for participant in participants:
        if participant.hackerrank_handle and participant.hackerrank_handle != '#N/A':
            url_exists, response_url = check_url_exists(
                f"https://www.hackerrank.com/profile/{participant.hackerrank_handle}"
            )
            if not url_exists:
                logging.debug(f"Retrying HackerRank URL check for participant {participant.handle}")
                url_exists, response_url = check_url_exists(
                    f"https://www.hackerrank.com/profile/{participant.hackerrank_handle}"
                )
            with open(HACKERRANK_FILE, 'a') as file:
                file.write(f"{participant.handle}, {participant.hackerrank_handle}, {url_exists}\n")
            logging.debug(f"Data written to file for participant {participant.handle}")
    logging.shutdown()
