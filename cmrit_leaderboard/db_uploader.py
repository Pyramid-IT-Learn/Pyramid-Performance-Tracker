import os
import pandas as pd
from cmrit_leaderboard.database import Database
from cmrit_leaderboard.config import CSV_FILE_PATH, CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE

db = Database()

def upload_to_db():
    # Load CSV file into dataframe
    df = pd.read_csv(
        CSV_FILE_PATH, 
        header=0, 
        names=['hallticketno', 'geeksforgeeksusername', 'codeforcesusername', 'leetcodeusername', 'codechefusername', 'hackerrankusername'], 
        converters={c: str.lower for c in ['hallticketno', 'geeksforgeeksusername', 'codeforcesusername', 'leetcodeusername', 'codechefusername', 'hackerrankusername']}
    )

    # Load the reports
    codechef = pd.read_csv(CODECHEF_FILE, names=['hallTicketNo', 'codechefUsername', 'codechefStatus'], sep=',\s*', engine='python')
    codeforces = pd.read_csv(CODEFORCES_FILE, names=['hallTicketNo', 'codeforcesUsername', 'codeforcesStatus'], sep=',\s*', engine='python')
    geeksforgeeks = pd.read_csv(GEEKSFORGEEKS_FILE, names=['hallTicketNo', 'geeksforgeeksUsername', 'geeksforgeeksStatus'], sep=',\s*', engine='python')
    hackerrank = pd.read_csv(HACKERRANK_FILE, names=['hallTicketNo', 'hackerrankUsername', 'hackerrankStatus'], sep=',\s*', engine='python')
    leetcode = pd.read_csv(LEETCODE_FILE, names=['hallTicketNo', 'leetcodeUsername', 'leetcodeStatus'], sep=',\s*', engine='python')

    # Set the index to 'hallTicketNo' for all reports
    codechef.set_index('hallTicketNo', inplace=True)
    codeforces.set_index('hallTicketNo', inplace=True)
    geeksforgeeks.set_index('hallTicketNo', inplace=True)
    hackerrank.set_index('hallTicketNo', inplace=True)
    leetcode.set_index('hallTicketNo', inplace=True)

    total_users = len(df)

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        print(f"Processing row {index + 1} of {total_users} with hallticketno {row['hallticketno']}...")

        hallticketno = row['hallticketno']
        geeksforgeeksusername = row['geeksforgeeksusername']
        codeforcesusername = row['codeforcesusername']
        leetcodeusername = row['leetcodeusername']
        codechefusername = row['codechefusername']
        hackerrankusername = row['hackerrankusername']

        # Get the status of the user from the reports
        codechefstatus = codechef.loc[hallticketno, 'codechefStatus'] if hallticketno in codechef.index else 'N/A'
        codeforcesstatus = codeforces.loc[hallticketno, 'codeforcesStatus'] if hallticketno in codeforces.index else 'N/A'
        geeksforgeeksstatus = geeksforgeeks.loc[hallticketno, 'geeksforgeeksStatus'] if hallticketno in geeksforgeeks.index else 'N/A'
        hackerrankstatus = hackerrank.loc[hallticketno, 'hackerrankStatus'] if hallticketno in hackerrank.index else 'N/A'
        leetcodestatus = leetcode.loc[hallticketno, 'leetcodeStatus'] if hallticketno in leetcode.index else 'N/A'

        # Create a dictionary of platform-specific details
        platform_details = {
            'codechefUsername': codechefusername,
            'codechefStatus': bool(codechefstatus),
            'codeforcesUsername': codeforcesusername,
            'codeforcesStatus': bool(codeforcesstatus),
            'geeksforgeeksUsername': geeksforgeeksusername,
            'geeksforgeeksStatus': bool(geeksforgeeksstatus),
            'hackerrankUsername': hackerrankusername,
            'hackerrankStatus': bool(hackerrankstatus),
            'leetcodeUsername': leetcodeusername,
            'leetcodeStatus': bool(leetcodestatus)
        }

        # Update the user in the database
        db.upsert_user(hallticketno, platform_details)
