# scripts/user.py

class User:
    def __init__(self, hall_ticket_no):
        self.hall_ticket_no = hall_ticket_no
        self.codechef_username = None
        self.codeforces_username = None
        self.geeksforgeeks_username = None
        self.hackerrank_username = None
        self.leetcode_username = None

    def update_username(self, platform, username):
        if platform == 'codechef':
            self.codechef_username = username
        elif platform == 'codeforces':
            self.codeforces_username = username
        elif platform == 'geeksforgeeks':
            self.geeksforgeeks_username = username
        elif platform == 'hackerrank':
            self.hackerrank_username = username
        elif platform == 'leetcode':
            self.leetcode_username = username
