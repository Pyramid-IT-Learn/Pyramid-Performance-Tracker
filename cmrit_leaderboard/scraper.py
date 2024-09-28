# cmrit_leaderboard/scraper.py

import pandas as pd

from scripts.codechef_scraper import scrape_codechef
from scripts.codeforces_scraper import scrape_codeforces
from scripts.geeksforgeeks_scraper import scrape_geeksforgeeks
from scripts.hackerrank_scraper import scrape_hackerrank
from scripts.leetcode_scraper import scrape_leetcode
from cmrit_leaderboard.config import CODECHEF_URL, CODEFORCES_URL, GEEKSFORGEEKS_URL, HACKERRANK_URL, LEETCODE_URL
from cmrit_leaderboard.database import Database

def scrape_all():
    scrape_platform('codechef')
    scrape_platform('codeforces')
    scrape_platform('geeksforgeeks')
    scrape_platform('hackerrank')
    scrape_platform('leetcode')

def scrape_platform(platform):
    url_map = {
        'codechef': CODECHEF_URL,
        'codeforces': CODEFORCES_URL,
        'geeksforgeeks': GEEKSFORGEEKS_URL,
        'hackerrank': HACKERRANK_URL,
        'leetcode': LEETCODE_URL
    }

    scrape_function_map = {
        'codechef': scrape_codechef,
        'codeforces': scrape_codeforces,
        'geeksforgeeks': scrape_geeksforgeeks,
        'hackerrank': scrape_hackerrank,
        'leetcode': scrape_leetcode
    }

    print(f'''
          =================================
          =========== {platform} ===========
          =================================
          ''')

    if platform in url_map and platform in scrape_function_map:
        url = url_map[platform]
        scraper_function = scrape_function_map[platform]

        # Get users from the database with platform-specific details
        db = Database()
        users = db.get_existing_users_for_platform(platform)

        users = pd.DataFrame(users)

        if len(users) == 0:
            print(f"No {platform} users found in the database.")
            return
        
        print(f"Found {len(users)} {platform} users in the database.")

        print(users)

        # Call the scraper function to update the users in the database
        users = scraper_function(users)

        users.replace({' ': ''}, regex=True, inplace=True)

        # Remove all columns that don't start with platform name, except hallTicketNo, TotalRating, Percentile
        users = users[users.columns[users.columns.str.startswith(platform) | users.columns.isin(['hallTicketNo', 'TotalRating', 'Percentile'])]]

        # Print columns
        print('--' * 30)
        print("The columns being uploaded are:")
        print(users.columns)
        print('--' * 30)

        # Update the database with the updated users
        db.upload_to_db_with_df(users)

