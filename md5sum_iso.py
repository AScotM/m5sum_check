import hashlib
import os

def calculate_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()

def check_md5sums(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if filename.lower().endswith('.iso'):
                md5_hash = calculate_md5(filepath)
                print(f"File: {filename}, MD5: {md5_hash}")

directory_path = '.'
check_md5sums(directory_path)

