# verifiers/hackerrank.py

import logging
import requests
from bs4 import BeautifulSoup
from cmrit_leaderboard.config import HACKERRANK_FILE, HACKERRANK_LOG_FILE, DEBUG
from time import sleep

def check_url_exists(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }
    try:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')

        # try to find community-content class within the soup, if found then the handle exists
        if soup.find("div", {"class": "community-content"}):
            print(f"Handle {url} exists, found the class community-content")
            return True, response.url

        # Extract the title of the page
        title = soup.title.string
        
        if "class=\"error-title\"" in str(soup):
            print(f"Handle {url} does not exist, found the class error-title")
            return False, response.url

        elif "HTTP 404: Page Not Found | HackerRank" in title:
            print(f"Handle {url} does not exist, found the title HTTP 404: Page Not Found | HackerRank")
            return False, response.url

        elif "class=\"e404-view\"" in str(soup):
            print(f"Handle {url} does not exist, found the class e404-view")
            return False, response.url

        # if the page contains the class class="page-not-found-container container" in the html, then the handle does not exist
        elif "class=\"page-not-found-container container\"" in str(soup):
            print(f"Handle {url} does not exist, found the class page-not-found-container")
            return False, response.url
        
        return True, response.url
    except requests.exceptions.RequestException:
        return False, "Exception"

def process_hackerrank(participants):
    logging.basicConfig(filename=HACKERRANK_LOG_FILE, level=logging.DEBUG)
    for participant in participants:
        print(f"Processing HackerRank handle {participant.hackerrank_handle} for participant {participant.handle}: ")
        url_exists = False
        if participant.hackerrank_handle and participant.hackerrank_handle != '#n/a':
            url_exists, response_url = check_url_exists(
                f"https://www.hackerrank.com/profile/{participant.hackerrank_handle}"
            )
            if not url_exists:
                logging.debug(f"Retrying HackerRank URL check for participant {participant.handle}")
                url_exists, response_url = check_url_exists(
                    f"https://www.hackerrank.com/profile/{participant.hackerrank_handle}"
                )
            print("")
        with open(HACKERRANK_FILE, 'a') as file:
            file.write(f"{participant.handle}, {participant.hackerrank_handle}, {url_exists}\n")
        logging.debug(f"Data written to file for participant {participant.handle}")
    logging.shutdown()
