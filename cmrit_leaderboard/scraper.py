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

        users.fillna(0, inplace=True)

        # Create a column for total rating
        users['TotalRating'] = users.get('codechefRating', 0) + users.get('codeforcesRating', 0) + users.get('geeksforgeeksWeeklyRating', 0) + users.get('geeksforgeeksPracticeRating', 0) + users.get('leetcodeRating', 0) + users.get('hackerrankRating', 0)

        try:
            max_codechef_rating = users.loc[users['codechefRating'].notnull(), 'codechefRating'].max()
        except KeyError:
            max_codechef_rating = 0

        try:
            max_codeforces_rating = users.loc[users['codeforcesRating'].notnull(), 'codeforcesRating'].max()
        except KeyError:
            max_codeforces_rating = 0

        try:
            max_geeksforgeeks_weekly_rating = users.loc[users['geeksforgeeksWeeklyRating'].notnull(), 'geeksforgeeksWeeklyRating'].max()
        except KeyError:
            max_geeksforgeeks_weekly_rating = 0

        try:
            max_geeksforgeeks_practice_rating = users.loc[users['geeksforgeeksPracticeRating'].notnull(), 'geeksforgeeksPracticeRating'].max()
        except KeyError:
            max_geeksforgeeks_practice_rating = 0

        try:
            max_leetcode_rating = users.loc[users['leetcodeRating'].notnull(), 'leetcodeRating'].max()
        except KeyError:
            max_leetcode_rating = 0

        try:
            max_hackerrank_rating = users.loc[users['hackerrankRating'].notnull(), 'hackerrankRating'].max()
        except KeyError:
            max_hackerrank_rating = 0

        for index, row in users.iterrows():
            cc = float(row.get('codechefRating', 0))
            cc = cc / max_codechef_rating * 100 if max_codechef_rating != 0 else 0
            cf = float(row.get('codeforcesRating', 0))
            cf = cf / max_codeforces_rating * 100 if max_codeforces_rating != 0 else 0
            ggw = float(row.get('geeksforgeeksWeeklyRating', 0))
            ggw = ggw / max_geeksforgeeks_weekly_rating * 100 if max_geeksforgeeks_weekly_rating != 0 else 0
            ggp = float(row.get('geeksforgeeksPracticeRating', 0))
            ggp = ggp / max_geeksforgeeks_practice_rating * 100 if max_geeksforgeeks_practice_rating != 0 else 0
            lc = float(row.get('leetcodeRating', 0))
            lc = lc / max_leetcode_rating * 100 if max_leetcode_rating != 0 else 0
            hr = float(row.get('hackerrankRating', 0))
            hr = hr / max_hackerrank_rating * 100 if max_hackerrank_rating != 0 else 0
            
            percentile = cc * 0.1 + cf * 0.3 + ggw * 0.3 + ggp * 0.1 + lc * 0.1 + hr * 0.1

            users.at[index, 'Percentile'] = percentile

        users.replace({' ': ''}, regex=True, inplace=True)

        # Update the database with the updated users
        db.upload_to_db_with_df(users)

