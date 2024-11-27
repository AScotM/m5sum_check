import hashlib
import os

def calculate_md5(file_path):

    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except OSError as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def check_md5sums(directory):

    try:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filename.lower().endswith('.iso'):
                md5_hash = calculate_md5(filepath)
                if md5_hash:
                    print(f"File: {filename}, MD5: {md5_hash}")
    except OSError as e:
        print(f"Error accessing directory {directory}: {e}")

if __name__ == "__main__":
    directory_path = '.'
    check_md5sums(directory_path)

