# verifiers/geeksforgeeks.py

import logging
import requests
from cmrit_leaderboard.config import GEKSFORGEEKS_FILE, DEBUG

def check_url_exists(url):
    try:
        response = requests.get(url)
        return response.status_code == 200, response.url
    except requests.RequestException as e:
        logging.error(f"Error checking URL {url}: {e}")
        return False, None

def process_geeksforgeeks(participants):
    logging.basicConfig(filename='geeksforgeeks_debug.log', level=logging.DEBUG)
    for participant in participants:
        if participant.geeksforgeeks_handle and participant.geeksforgeeks_handle != '#N/A':
            url_exists, response_url = check_url_exists(
                f"https://www.geeksforgeeks.org/user/{participant.geeksforgeeks_handle}"
            )
            with open(GEKSFORGEEKS_FILE, 'a') as file:
                file.write(f"{participant.handle}, {participant.geeksforgeeks_handle}, {url_exists}\n")
            logging.debug(f"Data written to file for participant {participant.handle}")
    logging.shutdown()
