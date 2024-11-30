import os
import hashlib

def get_file_hash(file_path, chunk_size=65536):
    """Generate a hash for a file."""
    hash_algo = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            while chunk:
                hash_algo.update(chunk)
                chunk = f.read(chunk_size)
        return hash_algo.hexdigest()
    except Exception as e:
        print(f"Error processing file: {file_path} | Error: {e}")
        return None

def find_duplicates(directory):
    """Find duplicate files in the specified directory."""
    file_hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            print(f"Processing file: {file_path}")
            file_hash = get_file_hash(file_path)

            if file_hash is None:
                continue  # Skip this file if there was an error

            if file_hash in file_hashes:
                duplicates.append((file_path, file_hashes[file_hash]))
            else:
                file_hashes[file_hash] = file_path

    return duplicates

def write_duplicates_to_file(duplicates, output_file):
    """Write the list of duplicates to a text file."""
    with open(output_file, 'w') as f:
        for dup1, dup2 in duplicates:
            f.write(f"Duplicate files:\n{dup1}\n{dup2}\n\n")

if __name__ == "__main__":
    # Specify the directory to search
    directory_to_search = "C:\\Users\\yanks\\Music\\AllMusic\\Artists"
    
    # Specify the output file location
    output_file = "C:\\Users\\yanks\\OneDrive\\Documents\\duplicate_files.txt"
    
    # Find duplicates
    duplicates = find_duplicates(directory_to_search)
    
    # Write duplicates to a text file
    write_duplicates_to_file(duplicates, output_file)
    
    print(f"Duplicate files have been written to {output_file}")
