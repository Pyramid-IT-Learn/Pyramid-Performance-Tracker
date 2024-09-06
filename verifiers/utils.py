# verifiers/utils.py

import os
import hashlib
import random
import string
import subprocess
import platform

def generate_random_string(length: int) -> str:
    """Generates a random string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_api_sig(rand: str, method_name: str, handles: str, time: int, secret: str, key: str) -> str:
    """Generates the API signature."""
    parameters = f"apiKey={key}&handles={handles}&time={time}"
    to_hash = f"{rand}/{method_name}?{parameters}#{secret}"
    
    hash_bytes = hashlib.sha512(to_hash.encode('utf-8')).digest()
    return ''.join(f"{byte:02x}" for byte in hash_bytes)

def sheet_download_if_not_exists(file_path, url):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Downloading the Username Sheet.")
    
        # Determine the operating system and set the command accordingly
        if platform.system() == "Windows":
            # Windows command using PowerShell
            command = [
                'powershell',
                '-Command',
                f'Invoke-WebRequest -Uri "{url}" -OutFile "{file_path}"'
            ]
        else:
            # Non-Windows command using wget
            command = [
                'wget',
                url,
                '-O', file_path
            ]

        # Execute the command
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Command executed successfully. Downloaded the Username Sheet.")
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred:", e)
            print("Error output:", e.stderr)
