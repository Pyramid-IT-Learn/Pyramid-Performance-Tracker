import re
import csv
import random
from cmrit_leaderboard.config import LIMIT_TEST

class Participant:
    handle = ""
    geeksforgeeks_handle = ""
    codeforces_handle = ""
    leetcode_handle = ""
    codechef_handle = ""
    hackerrank_handle = ""
    geeksforgeeks_url_exists = False
    codeforces_url_exists = False
    leetcode_url_exists = False
    codechef_url_exists = False
    hackerrank_url_exists = False

    def __init__(self, handle, geeksforgeeks_handle, codeforces_handle, leetcode_handle, codechef_handle,
                 hackerrank_handle, geeksforgeeks_url_exists=False, codeforces_url_exists=False, leetcode_url_exists=False, 
                 codechef_url_exists=False, hackerrank_url_exists=False):
        handle = remove_non_ascii(handle)
        geeksforgeeks_handle = remove_non_ascii(geeksforgeeks_handle)
        codeforces_handle = remove_non_ascii(codeforces_handle)
        leetcode_handle = remove_non_ascii(leetcode_handle)
        codechef_handle = remove_non_ascii(codechef_handle)
        hackerrank_handle = remove_non_ascii(hackerrank_handle)
        # Remove @ from the leetcode and hackerrank handles
        hackerrank_handle = hackerrank_handle.replace('@', '')
        leetcode_handle = leetcode_handle.replace('@', '')
        geeksforgeeks_handle = geeksforgeeks_handle.strip()
        # Remove . from all the handles
        geeksforgeeks_handle = geeksforgeeks_handle.replace('.', '')
        codeforces_handle = codeforces_handle.replace('.', '')
        leetcode_handle = leetcode_handle.replace('.', '')
        codechef_handle = codechef_handle.replace('.', '')
        hackerrank_handle = hackerrank_handle.replace('.', '')
        self.handle = handle
        self.geeksforgeeks_handle = geeksforgeeks_handle
        self.codeforces_handle = codeforces_handle
        self.leetcode_handle = leetcode_handle
        self.codechef_handle = codechef_handle
        self.hackerrank_handle = hackerrank_handle
        self.geeksforgeeks_url_exists = geeksforgeeks_url_exists
        self.codeforces_url_exists = codeforces_url_exists
        self.leetcode_url_exists = leetcode_url_exists
        self.codechef_url_exists = codechef_url_exists
        self.hackerrank_url_exists = hackerrank_url_exists

    def __str__(self):
        return f"{self.handle} => {self.geeksforgeeks_handle} => {self.codeforces_handle} => {self.leetcode_handle} => {self.codechef_handle} => {self.hackerrank_handle}"

def remove_non_ascii(input_string):
    return re.sub(r'[\t\n\x0B\f\r]+', '', input_string)

def load_participants(file_path):
    participants = []
    with open(file_path, 'r') as temp_file:
        temp_reader = csv.reader(temp_file)
        total_rows = sum(1 for _ in temp_reader) - 1  # Calculate total rows in the CSV
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        print(f"Total rows in CSV: {total_rows}")  # Print the total rows in the CSV
        
        # Load all participants into a list
        for count, row in enumerate(reader, start=1):
            if row[0] == "Roll number":  # Skip the header row
                continue
            if all(x == 'None' or x == '' for x in row):  # Stop if all cells in the row are empty
                break
            
            handle, geeksforgeeks_handle, codeforces_handle, leetcode_handle, codechef_handle, hackerrank_handle = map(str.lower, row)
            # Remove leading/trailing spaces and special characters
            participant = Participant(handle, geeksforgeeks_handle, codeforces_handle, leetcode_handle, codechef_handle,
                                      hackerrank_handle)  # Create Participant object
            participants.append(participant)  # Add Participant object to list
        
        if LIMIT_TEST:
            # Randomly select 30 participants
            participants = random.sample(participants, min(20, len(participants)))
            print("Limiting test to 30 participants")
            for participant in participants:
                print(participant)
        
        print("Finished loading participants")
        
    return participants
