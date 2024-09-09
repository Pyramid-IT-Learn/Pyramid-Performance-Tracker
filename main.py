import errno
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

from cmrit_leaderboard.config import DESCRIPTION, USERNAME_SHEET_URL, CSV_FILE_PATH, CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE
from cmrit_leaderboard.scraper import scrape_all, scrape_platform
from cmrit_leaderboard.leaderboard import Leaderboard
from cmrit_leaderboard.db_uploader import upload_to_db

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--scrape', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to scrape')
    parser.add_argument('--build', action='store_true', help='Build the leaderboard')
    parser.add_argument('--verify', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to verify')
    parser.add_argument('--clear', action='store_true', help='Clear the logs and reports directories')
    parser.add_argument('--upload', action='store_true', help='Upload data from CSV to database')

    args = parser.parse_args()

    if not any([args.scrape, args.build, args.verify, args.upload, args.clear]):
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

        if args.upload:
            # Make sure reports directory exists and has all the required files
            if os.path.exists('reports'):
                required_files = [CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE]
                for file in required_files:
                    if not os.path.exists(f'{file}'):
                        print(f"File '{file}' is missing. Please run the verifier script again.")
                        exit()
            else:
                print("Directory 'reports' does not exist. Please run the verifier script again.")
                exit()

            print("Uploading data to database...")
            # Call the function from db_uploader to process CSV and update the database
            upload_to_db()

        if args.clear:
            for folder in ['logs', 'reports']:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            try:
                                os.unlink(file_path)
                            except OSError as e:
                                print('Failed to delete %s. Reason: %s' % (file_path, e))
                                print('Trying to clear the contents of the directory...')
                                if e.errno == errno.EACCES:
                                    with open(file_path, 'w'):
                                        pass
                                else:
                                    raise
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == "__main__":
    main()
