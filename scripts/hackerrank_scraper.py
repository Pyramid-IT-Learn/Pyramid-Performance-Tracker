# scripts/hackerrank_scraper.py

import urllib.parse
import json
import requests
from cmrit_leaderboard.config import Config, HACKERRANK_URL, HACKERRANK_CONTEST_URLS, HACKERRANK_API_URL

def scrape_hackerrank(users):
    # Create hackerrankRating column
    users['hackerrankRating'] = 0
    # Load the contest name from urls and store in a list
    SEARCH_TOKENS = [url.split('/')[-1] for url in HACKERRANK_CONTEST_URLS[Config.USERS_COLLECTION]]

    for token in SEARCH_TOKENS:
        for i in range(1, 10000, 100):
            # String url = "https://www.hackerrank.com/rest/contests/" + trackerName + "/leaderboard?offset=" + j + "&limit=100";                url = f"{HACKERRANK_API_URL
            url = f"{HACKERRANK_API_URL}/{token}/leaderboard?offset={i}&limit=100"
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "TE": "Trailers"
            }

            print(url)

            response = requests.get(url, headers=header)

            response_json = response.json()

            if response_json['models'] == []:
                break

            hackerrank_users_set = set()

            for user in users['hackerrankUsername']:
                hackerrank_users_set.add(user.lower())

            for hackerrank_user in response_json['models']:
                hackerrank_username = hackerrank_user['hacker'].lower()
                if hackerrank_username in hackerrank_users_set:
                    users.loc[users['hackerrankUsername'] == hackerrank_username, 'hackerrankRating'] += hackerrank_user['score']
                print(f"Found user {hackerrank_user['hacker']} with rating {hackerrank_user['score']}")

            print(f"Done with {token} leaderboard offset {i} - {i+100}")

    print(users[['hallTicketNo', 'hackerrankUsername', 'hackerrankRating']])

    return users

