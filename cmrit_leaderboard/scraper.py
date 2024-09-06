# cmrit_leaderboard/scraper.py

from scripts.codechef_scraper import scrape_codechef
from scripts.codeforces_scraper import scrape_codeforces
from scripts.geeksforgeeks_scraper import scrape_geeksforgeeks
from scripts.hackerrank_scraper import scrape_hackerrank
from scripts.leetcode_scraper import scrape_leetcode
from cmrit_leaderboard.config import CODECHEF_URL, CODEFORCES_URL, GEEKSFORGEEKS_URL, HACKERRANK_URL, LEETCODE_URL
from cmrit_leaderboard.database import Database
from scripts.user import User

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

    if platform in url_map and platform in scrape_function_map:
        url = url_map[platform]
        scraper_function = scrape_function_map[platform]

        # Get users from the database with platform-specific details
        db = Database()
        users = db.get_users_with_usernames(platform)

        user_objects = {user['hallTicketNo']: User(user['hallTicketNo']) for user in users}

        # Call the scraper function with URL and users
        scraped_data = scraper_function(url, user_objects)

        # Update database with scraped data
        for hall_ticket_no, user_data in scraped_data.items():
            db.upsert_user(hall_ticket_no, user_data)
