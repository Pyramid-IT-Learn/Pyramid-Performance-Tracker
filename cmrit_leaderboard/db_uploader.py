import os
import pandas as pd
from cmrit_leaderboard.database import Database
from cmrit_leaderboard.config import Config, CODECHEF_FILE, CODEFORCES_FILE, GEEKSFORGEEKS_FILE, HACKERRANK_FILE, LEETCODE_FILE
from verifiers.participant import Participant

def upload_to_db(is_test=False, test_participants: list[Participant] = None):
    # Moved this line here to avoid pusing to same database multiple times when running for multiple batches
    db = Database() 

    if is_test:
        # Initialize df with columns
        df = pd.DataFrame(columns=['hallTicketNo', 'geeksforgeeksUsername', 'codeforcesUsername', 'leetcodeUsername', 'codechefUsername', 'hackerrankUsername'])
        # Load test participants
        for participant in test_participants:
            df = df._append({
                'hallTicketNo': participant.handle,
                'geeksforgeeksUsername': participant.geeksforgeeks_handle,
                'codeforcesUsername': participant.codeforces_handle,
                'leetcodeUsername': participant.leetcode_handle,
                'codechefUsername': participant.codechef_handle,
                'hackerrankUsername': participant.hackerrank_handle
            }, ignore_index=True)
    else:
        # Load CSV file into dataframe
        df = pd.read_csv(
            Config.CSV_FILE_PATH, 
            header=0, 
            names=['hallTicketNo', 'geeksforgeeksUsername', 'codeforcesUsername', 'leetcodeUsername', 'codechefUsername', 'hackerrankUsername'], 
            converters={
                c: lambda x: x.lower().replace('@', '') 
                for c in ['hallTicketNo', 'geeksforgeeksUsername', 'codeforcesUsername', 'leetcodeUsername', 'codechefUsername', 'hackerrankUsername']
            }
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
        print(f"Processing row {index + 1} of {total_users} with hallticketno {row['hallTicketNo']}...")

        hallticketno = row['hallTicketNo']
        geeksforgeeksusername = row['geeksforgeeksUsername']
        codeforcesusername = row['codeforcesUsername']
        leetcodeusername = row['leetcodeUsername']
        codechefusername = row['codechefUsername']
        hackerrankusername = row['hackerrankUsername']

        def get_status(hallticketno, df, status_column):
            if hallticketno in df.index:
                status = df.at[hallticketno, status_column]
                print("--" * 10)
                print(f'For {hallticketno}, {status_column} = {status}')
                
                # Check if status is a Series and get the first value if so
                if isinstance(status, pd.Series):
                    print("Is a series")
                    status = status.iloc[0]
                
                print(status)
                print(type(status))
                print("--" * 10)
                
                return bool(status) if pd.notnull(status) else None
            return None


        # Get the status of the user from the reports
        codechefstatus = get_status(hallticketno, codechef, 'codechefStatus')
        codeforcesstatus = get_status(hallticketno, codeforces, 'codeforcesStatus')
        geeksforgeeksstatus = get_status(hallticketno, geeksforgeeks, 'geeksforgeeksStatus')
        hackerrankstatus = get_status(hallticketno, hackerrank, 'hackerrankStatus')
        leetcodestatus = get_status(hallticketno, leetcode, 'leetcodeStatus')

        # Create a dictionary of platform-specific details
        platform_details = {
            'codechefUsername': codechefusername,
            'codechefStatus': codechefstatus,
            'codeforcesUsername': codeforcesusername,
            'codeforcesStatus': codeforcesstatus,
            'geeksforgeeksUsername': geeksforgeeksusername,
            'geeksforgeeksStatus': geeksforgeeksstatus,
            'hackerrankUsername': hackerrankusername,
            'hackerrankStatus': hackerrankstatus,
            'leetcodeUsername': leetcodeusername,
            'leetcodeStatus': leetcodestatus
        }
        # Update the user in the database
        db.upsert_user(hallticketno, platform_details)

