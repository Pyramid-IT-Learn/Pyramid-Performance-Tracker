# cmrit_leaderboard/leaderboard.py

import pandas as pd
from cmrit_leaderboard.config import LEADERBOARD_REPORT_FILE
from cmrit_leaderboard.database import Database

class Leaderboard:
    def __init__(self):
        self.db = Database()

    def build_leaderboard(self):
        # Example: Fetch all Users
        users = self.db.get_all_users()
        data = []

        for user in users:
            data.append({
                'Hall Ticket No': user['hallTicketNo'],
                'CodeChef Username': user.get('codechefUsername', 'N/A'),
                'CodeChef Rating': user.get('codechefRating', 'N/A'),
                'Codeforces Username': user.get('codeforcesUsername', 'N/A'),
                'Codeforces Rating': user.get('codeforcesRating', 'N/A'),
                'GeeksforGeeks Username': user.get('geeksforgeeksUsername', 'N/A'),
                'GeeksforGeeks Rating': user.get('geeksforgeeksRating', 'N/A'),
                'Leetcode Username': user.get('leetcodeUsername', 'N/A'),
                'Leetcode Rating': user.get('leetcodeRating', 'N/A'),
                'Hackerrank Username': user.get('hackerrankUsername', 'N/A'),
                'Hackerrank Rating': user.get('hackerrankRating', 'N/A'),
            })

        df = pd.DataFrame(data)
        df.to_excel(LEADERBOARD_REPORT_FILE, index=False)
