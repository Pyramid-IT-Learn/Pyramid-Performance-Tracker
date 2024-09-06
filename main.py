# cmrit_leaderboard/main.py

import csv
import argparse

from verifiers.codechef import process_codechef
from verifiers.codeforces import process_codeforces
from verifiers.geeksforgeeks import process_geeksforgeeks
from verifiers.hackerrank import process_hackerrank
from verifiers.leetcode import process_leetcode
from verifiers.utils import sheet_download_if_not_exists
from verifiers.participant import load_participants

from cmrit_leaderboard.config import DESCRIPTION, USERNAME_SHEET_URL, CSV_FILE_PATH
from cmrit_leaderboard.scraper import scrape_all, scrape_platform
from cmrit_leaderboard.leaderboard import Leaderboard

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--scrape', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to scrape')
    parser.add_argument('--build', action='store_true', help='Build the leaderboard')
    parser.add_argument('--verify', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to verify')

    args = parser.parse_args()

    if not any([args.scrape, args.build, args.verify]):
        parser.print_help()
    else:
        if args.scrape:
            if args.scrape == 'all':
                scrape_all()
            else:
                scrape_platform(args.scrape)

        if args.build:
            leaderboard = Leaderboard()
            leaderboard.build_leaderboard()

        if args.verify:
            url = USERNAME_SHEET_URL
            file_path = CSV_FILE_PATH

            sheet_download_if_not_exists(file_path, url)

            participants = load_participants(file_path)

            if args.verify == 'codechef' or args.verify == 'all':
                process_codechef(participants)

            if args.verify == 'codeforces' or args.verify == 'all':
                process_codeforces(participants)

            if args.verify == 'geeksforgeeks' or args.verify == 'all':
                process_geeksforgeeks(participants)

            if args.verify == 'hackerrank' or args.verify == 'all':
                process_hackerrank(participants)

            if args.verify == 'leetcode' or args.verify == 'all':
                process_leetcode(participants)

if __name__ == "__main__":
    main()

