# cmrit_leaderboard/main.py

import os
import argparse
import shutil

print("Maintaining directories...")
if not os.path.exists('logs'):
    print(f"Directory 'logs' does not exist. Creating it...")
    os.makedirs('logs')
if not os.path.exists('reports'):
    print(f"Directory 'reports' does not exist. Creating it...")
    os.makedirs('reports')

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
    parser.add_argument('--clear', action='store_true', help='Clear the logs and reports directories')

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

        if args.clear:
            for folder in ['logs', 'reports']:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    main()


