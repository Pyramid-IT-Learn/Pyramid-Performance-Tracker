# verifiers/codechef.py

import logging
import requests
from cmrit_leaderboard.config import CODECHEF_FILE, DEBUG
from time import sleep

def check_url_exists(url):
    try:
        response = requests.get(url)
        return response.status_code == 200, response.url
    except requests.RequestException as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False, None

def process_codechef(participants):
    logging.basicConfig(filename='codechef_debug.log', level=logging.DEBUG)
    for participant in participants:
        if participant.codechef_handle and participant.codechef_handle != '#N/A':
            url_exists, response_url = check_url_exists(
                f"https://code-chef-rating-api.vercel.app/{participant.codechef_handle}"
            )
            sleep(8)
            if not url_exists:
                logging.debug(f"Retrying CodeChef URL check for participant {participant.handle}")
                url_exists, response_url = check_url_exists(
                    f"https://code-chef-rating-api.vercel.app/{participant.codechef_handle}"
                )
            with open(CODECHEF_FILE, 'a') as file:
                file.write(f"{participant.handle}, {participant.codechef_handle}, {url_exists}\n")
            logging.debug(f"Data written to file for participant {participant.handle}")
    logging.shutdown()
