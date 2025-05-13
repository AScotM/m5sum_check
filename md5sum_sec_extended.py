import hashlib
from pathlib import Path
import argparse
import sys


def calculate_hash(file_path, algorithm="md5", verbose=False):
    try:
        hasher = hashlib.new(algorithm)
    except ValueError:
        print(f"Unsupported algorithm: {algorithm}")
        return None

    try:
        with file_path.open('rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except OSError as e:
        if verbose:
            print(f"Error reading {file_path}: {e}")
        return None


def check_hashes(directory, exts, algorithm="md5", output_file=None, verbose=False):
    results = []

    for ext in exts:
        for file_path in Path(directory).rglob(f'*{ext}'):
            if file_path.is_file():
                if verbose:
                    print(f"Processing: {file_path}")
                hash_val = calculate_hash(file_path, algorithm=algorithm, verbose=verbose)
                if hash_val:
                    line = f"{hash_val}  {file_path.name}"
                    print(line)
                    results.append(line)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(results) + '\n')
            if verbose:
                print(f"Hashes written to {output_file}")
        except OSError as e:
            print(f"Error writing to {output_file}: {e}")


def verify_hashes(file_path, algorithm="md5", verbose=False):
    """
    Verifies hashes in a file (like `md5sum -c` behavior).
    Format per line: <hash> <two spaces> <filename>
    """
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split("  ")
                if len(parts) != 2:
                    print(f"Invalid line format: {line.strip()}")
                    continue

                expected_hash, filename = parts
                filepath = Path(filename)
                if not filepath.exists():
                    print(f"{filename}: NOT FOUND")
                    continue

                actual_hash = calculate_hash(filepath, algorithm=algorithm, verbose=verbose)
                if actual_hash == expected_hash:
                    print(f"{filename}: OK")
                else:
                    print(f"{filename}: FAILED")
    except OSError as e:
        print(f"Error verifying hashes: {e}")


def main():
    parser = argparse.ArgumentParser(description="Compute or verify checksums of files.")
    parser.add_argument("directory", nargs="?", default=".", help="Directory to scan for files.")
    parser.add_argument("-a", "--algorithm", choices=["md5", "sha256"], default="md5", help="Hash algorithm to use.")
    parser.add_argument("-e", "--ext", nargs="+", default=[".iso"], help="File extensions to include (e.g. .iso .img)")
    parser.add_argument("-o", "--output", help="Write hashes to a file.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    parser.add_argument("-c", "--check", metavar="FILE", help="Verify hashes from a file (like md5sum -c).")

    args = parser.parse_args()

    if args.check:
        verify_hashes(args.check, algorithm=args.algorithm, verbose=args.verbose)
    else:
        check_hashes(args.directory, args.ext, algorithm=args.algorithm, output_file=args.output, verbose=args.verbose)


if __name__ == "__main__":
    main()
