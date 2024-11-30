import os
import hashlib

# Define the directory to search and the output file path
search_directory = r"C:\Users\yanks\Music\iTunes\iTunes Media\Music"
output_file_path = r"C:\Users\yanks\OneDrive\Documents\duplicate_files.txt"

def calculate_file_hash(file_path, chunk_size=8192):
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_sha256.update(chunk)
    except (OSError, IOError):
        return None
    return hash_sha256.hexdigest()

def find_duplicates(directory, max_files=None):
    """Find duplicate files in the given directory."""
    file_hashes = {}
    duplicates = []
    file_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip hidden or system files
            if file.startswith(".") or file.startswith("~"):
                continue

            # Calculate hash and check for duplicates
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                if file_hash in file_hashes:
                    duplicates.append((file_hashes[file_hash], file_path))
                else:
                    file_hashes[file_hash] = file_path

            # Log progress
            file_count += 1
            if file_count % 100 == 0:
                print(f"Processed {file_count} files...")

            # Stop if max_files is reached (for debugging purposes)
            if max_files and file_count >= max_files:
                print("Reached file limit for debugging.")
                return duplicates

    return duplicates

def write_duplicates_to_file(duplicates, output_path):
    """Write duplicate files to a text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        if duplicates:
            f.write("Duplicate Files Found:\n\n")
            for original, duplicate in duplicates:
                f.write(f"Original: {original}\nDuplicate: {duplicate}\n\n")
        else:
            f.write("No duplicate files found.\n")

def main():
    # You can set a max_files limit for testing/debugging
    max_files_to_process = None  # Set to an integer for testing, or None for full run
    duplicates = find_duplicates(search_directory, max_files=max_files_to_process)
    write_duplicates_to_file(duplicates, output_file_path)
    print(f"Duplicate file report saved to: {output_file_path}")

if __name__ == "__main__":
    main()

