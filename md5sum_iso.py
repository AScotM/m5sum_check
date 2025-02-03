import hashlib
import pathlib
import io

def calculate_md5(file_path):
    """Calculate MD5 checksum for a given file."""
    md5 = hashlib.md5()
    try:
        with file_path.open('rb') as f:
            for chunk in iter(lambda: f.read(io.DEFAULT_BUFFER_SIZE), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except (OSError, IOError) as e:
        return f"Error: {e}"

def check_md5sums(directory):
    """Scan a directory for `.iso` files and calculate their MD5 hashes."""
    dir_path = pathlib.Path(directory)
    
    for file in dir_path.iterdir():
        if file.is_file() and file.suffix.lower() == '.iso':
            md5_hash = calculate_md5(file)
            print(f"{file.name:40} MD5: {md5_hash}")

# Run function in current directory
if __name__ == "__main__":
    check_md5sums(pathlib.Path("."))
