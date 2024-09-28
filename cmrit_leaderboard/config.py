import os

# API and Database configuration
API_KEY = os.getenv('CODEFORCES_KEY')
API_SECRET = os.getenv('CODEFORCES_SECRET')
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_PASSWORD = os.getenv('GIT_PASSWORD')
GFG_USERNAME = os.getenv("GFG_USERNAME")
GFG_PASSWORD = os.getenv("GFG_PASSWORD")
CODECHEF_CLIENT_ID = os.getenv("CODECHEF_CLIENT_ID")
CODECHEF_CLIENT_SECRET = os.getenv("CODECHEF_CLIENT_SECRET")
DB_PASSWORD = os.getenv("DB_PASSWORD")
MONGODB_URI = f'mongodb://myUserAdmin:{DB_PASSWORD}@103.172.179.23:27017/'
DESCRIPTION = 'Pyramid Leaderboard Scraper'

# Debugging
DEBUG = True
LIMIT_TEST = False

class Config:
    DB_NAME = None
    USERS_COLLECTION = None
    USERNAME_SHEET_URL = None
    CSV_FILE_PATH = None

DB_MAPPING = {
    "1": {
        "DB_NAME": "CMRIT",
        "USERS_COLLECTION": "CMRIT-2025-LEADERBOARD",
        "USERNAME_SHEET_URL": "https://docs.google.com/spreadsheets/d/17ypZiX6LzgmADqSgDmQ3vytIrf1DkEHafIltWaXRlog/pub?output=csv&gid=0&single=true",
        "CSV_FILE_PATH" : 'data/CMRIT2025Leaderbaord.csv'
    },
    "2": {
        "DB_NAME": "CMRIT",
        "USERS_COLLECTION": "CMRIT-2026-LEADERBOARD",
        "USERNAME_SHEET_URL": "https://docs.google.com/spreadsheets/d/1UEPRw2UcWdw4ZpmO4qZ6nOhpCygz_MWqtgvO1ugWf_E/pub?output=csv&gid=0&single=true",
        "CSV_FILE_PATH" : 'data/CMRIT2026Leaderbaord.csv'
    },
    "3": {
        "DB_NAME": "CMRIT",
        "USERS_COLLECTION": "CMRIT-2027-LEADERBOARD",
        "USERNAME_SHEET_URL": "https://docs.google.com/spreadsheets/u/2/d/e/2PACX-1vRsneoGOzu7L_Qh5M5fuZNf97fc2kVIum0w_oslizePKgRhR9pJi4EWNv5tPV7TGuvl-F_Q9rgRFBkQ/pub?output=csv&gid=0&single=true",
        "CSV_FILE_PATH" : 'data/CMRIT2027Leaderbaord.csv'
    },
}

# Hackerrank Contest URLs
# Each key corresponds to a USERS_COLLECTION name from the DB_MAPPING.
# The values are lists of contest URLs associated with that collection.
# Ensure that the key matches the USERS_COLLECTION exactly (e.g., "CMRIT-2026-LEADERBOARD").
# Do not leave trailing slashes in the URLs (e.g., "https://www.hackerrank.com/cmrit26-1-basics" ✅, 
# "https://www.hackerrank.com/cmrit26-2-lpb/" ❌).
HACKERRANK_CONTEST_URLS = {
    "CMRIT-2025-LEADERBOARD": [
        "https://www.hackerrank.com/cmrit25-1-basics",
        "https://www.hackerrank.com/cmrit25-4-rbd",
        "https://www.hackerrank.com/cmrit25-3-iterables",
        "https://www.hackerrank.com/cmrit25-2-lpb",
        "https://www.hackerrank.com/cmrit25-5-ds",
        "https://www.hackerrank.com/1-basics-2025",
        "https://www.hackerrank.com/2-loops-2025",
        "https://www.hackerrank.com/3-bitpat-2025",
        "https://www.hackerrank.com/4-iterables-2025",
        "https://www.hackerrank.com/5-recursion-2025",
        "https://www.hackerrank.com/strivers-sde-sheet",
        "https://www.hackerrank.com/ds-2025",
        "https://www.hackerrank.com/codevita-2025",
        "https://www.hackerrank.com/mentor-graphics-2025"
    ],
    "CMRIT-2026-LEADERBOARD": [
        "https://www.hackerrank.com/cmrit26-1-basics",
        "https://www.hackerrank.com/cmrit26-2-lpb",
        "https://www.hackerrank.com/cmrit-2y-2026",
        "https://www.hackerrank.com/cmrit-may-2024",
        "https://www.hackerrank.com/cmrit-june-2024",
        "https://www.hackerrank.com/cmrit-august-2024",
        "https://www.hackerrank.com/cmrit-september-2024"
    ],
    "CMRIT-2027-LEADERBOARD": []  # No contests added yet for 2027
}

# Scraper URLs
CODECHEF_URL = 'https://www.codechef.com/users'
CODEFORCES_URL = 'https://codeforces.com/api'
GEEKSFORGEEKS_URL = 'https://auth.geeksforgeeks.org/user'
GFG_WEEKLY_CONTEST_URL = "https://practiceapi.geeksforgeeks.org/api/latest/events/recurring/gfg-weekly-coding-contest/leaderboard/?leaderboard_type=0&page="
GFG_PRACTICE_URL = "https://practiceapi.geeksforgeeks.org/api/v1/institute/341/students/stats?page_size=100000&page="
GFG_API_URL = "https://authapi.geeksforgeeks.org/api-get/user-profile-info/?handle="
HACKERRANK_URL = 'https://www.hackerrank.com/'
HACKERRANK_API_URL = 'https://www.hackerrank.com/rest/contests'
LEETCODE_URL = 'https://leetcode.com/'
CODECHEF_API_URL = 'https://api.codechef.com/'

# File paths
HACKERRANK_URLS_FILE = 'data/hackerrank_urls.txt'
PARTICIPANT_DETAILS_FILE = 'data/participant_details.csv'
LEADERBOARD_REPORT_FILE = f'reports/GeneratedReport.xlsx'

GEEKSFORGEEKS_FILE = 'reports/geeksforgeeks_handles.txt'
CODEFORCES_FILE = 'reports/codeforces_handles.txt'
LEETCODE_FILE = 'reports/leetcode_handles.txt'
CODECHEF_FILE = 'reports/codechef_handles.txt'
HACKERRANK_FILE = 'reports/hackerrank_handles.txt'

# Leetcode Query
# Try not to modify this
LEETCODE_QUERY = '''
https://leetcode.com/graphql?query=query
{     
      userContestRanking(username:  "{<username>}") 
      {
        attendedContestsCount
        rating
        globalRanking
        totalParticipants
        topPercentage    
      }
}
'''


# Chrome driver version
CHROME_DRIVER_VERSION = 128

# Maximum number of requests per second
MAX_REQUESTS_PER_SECOND = 2

# Rate limiter configuration
MAX_CALLS_PER_MINUTE = 30
SECONDS_PER_MINUTE = 300
CALL_INTERVAL = SECONDS_PER_MINUTE / MAX_CALLS_PER_MINUTE
