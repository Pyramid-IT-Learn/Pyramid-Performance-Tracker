import os

# API and Database configuration
API_KEY = os.getenv('CODEFORCES_KEY')
API_SECRET = os.getenv('CODEFORCES_SECRET')
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_PASSWORD = os.getenv('GIT_PASSWORD')
GFG_USERNAME = os.getenv("GFG_USERNAME")
GFG_PASSWORD = os.getenv("GFG_PASSWORD")
MONGODB_URI = 'mongodb://localhost:27017/'
DB_NAME = 'CMRIT-2026-LEADERBOARD'
USERS_COLLECTION = 'USERS'

# Debugging
DEBUG = True

# Project settings
DESCRIPTION = 'CMRIT 2026 Leaderboard'
USERNAME_SHEET_URL = 'https://docs.google.com/spreadsheets/d/1UEPRw2UcWdw4ZpmO4qZ6nOhpCygz_MWqtgvO1ugWf_E/pub?output=csv&gid=0&single=true'

# Scraper URLs
CODECHEF_URL = 'https://www.codechef.com/users'
CODEFORCES_URL = 'https://codeforces.com/api'
GEEKSFORGEEKS_URL = 'https://auth.geeksforgeeks.org/user'
GFG_WEEKLY_CONTEST_URL = "https://practiceapi.geeksforgeeks.org/api/latest/events/recurring/gfg-weekly-coding-contest/leaderboard/?leaderboard_type=0&page="
GFG_PRACTICE_URL = "https://practiceapi.geeksforgeeks.org/api/v1/institute/341/students/stats?page_size=100000&page="
HACKERRANK_URL = 'https://www.hackerrank.com/'
HACKERRANK_API_URL = 'https://www.hackerrank.com/rest/contests'
LEETCODE_URL = 'https://leetcode.com/'
CODECHEF_API_URL = 'https://code-chef-rating-api.vercel.app/'

# File paths
HACKERRANK_URLS_FILE = 'data/hackerrank_urls.txt'
PARTICIPANT_DETAILS_FILE = 'data/participant_details.csv'
LEADERBOARD_REPORT_FILE = 'reports/CurrentCMRITLeaderboard2026.xlsx'
EXCEL_FILE_PATH = 'data/CMRIT2026Leaderbaord.xlsx'
CSV_FILE_PATH = 'data/CMRIT2026Leaderbaord.csv'

GEEKSFORGEEKS_FILE = 'reports/geeksforgeeks_handles.txt'
CODEFORCES_FILE = 'reports/codeforces_handles.txt'
LEETCODE_FILE = 'reports/leetcode_handles.txt'
CODECHEF_FILE = 'reports/codechef_handles.txt'
HACKERRANK_FILE = 'reports/hackerrank_handles.txt'

GEEKSFORGEEKS_LOG_FILE = 'logs/geeksforgeeks.log'
CODEFORCES_LOG_FILE = 'logs/codeforces.log'
LEETCODE_LOG_FILE = 'logs/leetcode.log'
CODECHEF_LOG_FILE = 'logs/codechef.log'
HACKERRANK_LOG_FILE = 'logs/hackerrank.log'

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

# Hackerrank Contest URLs
# Do not leave trailing slashes
# Meaning no / at the end of the URL
# Example:
# "https://www.hackerrank.com/cmrit26-1-basics" ✅
# "https://www.hackerrank.com/cmrit26-2-lpb/" ❌
HACKERRANK_CONTEST_URLS = [
    "https://www.hackerrank.com/cmrit26-1-basics",
    "https://www.hackerrank.com/cmrit26-2-lpb",
    "https://www.hackerrank.com/cmrit-2y-2026",
    "https://www.hackerrank.com/cmrit-may-2024",
    "https://www.hackerrank.com/cmrit-june-2024",
    "https://www.hackerrank.com/cmrit-august-2024"
]


# Chrome driver version
CHROME_DRIVER_VERSION = 128

# Maximum number of requests per second
MAX_REQUESTS_PER_SECOND = 2

# Rate limiter configuration
MAX_CALLS_PER_MINUTE = 10
SECONDS_PER_MINUTE = 60
CALL_INTERVAL = SECONDS_PER_MINUTE / MAX_CALLS_PER_MINUTE
