import re
import csv

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
        # remove @ from the leeetcode handle
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


def remove_non_ascii(input_string):
    return re.sub(r'[\t\n\x0B\f\r]+', '', input_string)


def load_participants(file_path):
    participants = []
    with open(file_path, 'r') as temp_file:
        temp_reader = csv.reader(temp_file)  # Create a temporary reader to count total rows
        total_rows = sum(1 for _ in temp_reader) - 1  # Calculate total rows in the CSV
        # close the temporary file
        temp_file.close()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        print(f"Total rows in CSV: {total_rows}")  # Print the total rows in the CSV
        count = 1
        for row in reader:
            if row[0] == "Roll number":  # Skip the header row
                continue
            if all(x == 'None' or x == '' for x in row):  # Stop if all cells in the row are empty
                break
            handle, geeksforgeeks_handle, codeforces_handle, leetcode_handle, codechef_handle, hackerrank_handle = row
            # convert all the handles to lowercase
            handle = handle.lower()
            geeksforgeeks_handle = geeksforgeeks_handle.lower()
            codeforces_handle = codeforces_handle.lower()
            leetcode_handle = leetcode_handle.lower()
            codechef_handle = codechef_handle.lower()
            hackerrank_handle = hackerrank_handle.lower()
            print(f"( {count} / {total_rows} ) Loading participant {handle}")  # Print progress
            participant = Participant(handle, geeksforgeeks_handle, codeforces_handle, leetcode_handle, codechef_handle,
                                    hackerrank_handle)  # Create Participant object
            participants.append(participant)  # Add Participant object to list
            count += 1
    print("Finished loading participants")
    file.close()
    return participants