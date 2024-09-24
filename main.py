import errno
import os
import argparse
import shutil
import pandas as pd

print("Maintaining directories...")
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

from cmrit_leaderboard.config import Config, DESCRIPTION, DB_MAPPING, CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE, LIMIT_TEST
from cmrit_leaderboard.scraper import scrape_all, scrape_platform
from cmrit_leaderboard.leaderboard import Leaderboard
from cmrit_leaderboard.evaluator import evaluate_leaderboard

def maintain_directories():
    print("Maintaining directories...")
    if not os.path.exists('reports'):
        print(f"Directory 'reports' does not exist. Creating it...")
        os.makedirs('reports')

def main():
    maintain_directories()

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--batch', choices=DB_MAPPING.keys(), help='Select a specific batch to run (default is all)', default=None)
    parser.add_argument('--all-batches', action='store_true', help='Run all batches sequentially')
    parser.add_argument('--scrape', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to scrape')
    parser.add_argument('--build', action='store_true', help='Build the leaderboard')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate the leaderboard')
    parser.add_argument('--verify', choices=['all', 'codechef', 'codeforces', 'geeksforgeeks', 'hackerrank', 'leetcode'], help='Platform to verify')
    parser.add_argument('--clear', action='store_true', help='Clear the logs and reports directories')
    parser.add_argument('--upload', action='store_true', help='Upload data from CSV to database')

    args = parser.parse_args()

    if args.all_batches:
        for batch_key in DB_MAPPING.keys():
            run_for_batch(batch_key, args)
            clear_directories()  # Clear after each batch
    elif args.batch:
        run_for_batch(args.batch, args)
    else:
        parser.print_help()

def run_for_batch(batch_key, args):
    batch_config = DB_MAPPING[batch_key]
    Config.DB_NAME = batch_config["DB_NAME"]
    Config.USERS_COLLECTION = batch_config["USERS_COLLECTION"]
    Config.USERNAME_SHEET_URL = batch_config["USERNAME_SHEET_URL"]
    Config.CSV_FILE_PATH = batch_config["CSV_FILE_PATH"]

    print(f"\nRunning for batch: {batch_key} => {Config.DB_NAME} - {Config.USERS_COLLECTION}")

    if args.clear:
        clear_directories()

    from cmrit_leaderboard.db_uploader import upload_to_db  # Import here to avoid circular imports

    file_path = Config.CSV_FILE_PATH
    sheet_download_if_not_exists(file_path, Config.USERNAME_SHEET_URL)
    participants = load_participants(file_path)
    
    if args.verify:
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
        sheet_download_if_not_exists(file_path, Config.USERNAME_SHEET_URL)
        check_required_files()
        print("Uploading data to database...")
        upload_to_db(is_test=LIMIT_TEST, test_participants=participants if participants else None)

    if args.scrape:
        if args.scrape == 'all':
            scrape_all()
        else:
            scrape_platform(args.scrape)

    if args.build:
        leaderboard = Leaderboard()
        leaderboard_data = leaderboard.build_leaderboard()

    if args.evaluate:  # Check if evaluation is requested
        evaluate_leaderboard()
        print(f'Evaluation completed for {Config.DB_NAME} - {Config.USERS_COLLECTION}')

def check_required_files():
    required_files = [CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE]
    for file in required_files:
        if not os.path.exists(file):
            print(f"File '{file}' is missing. Please run the verifier script again.")
            exit(0)

def clear_directories():
    for folder in ['reports']:
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
