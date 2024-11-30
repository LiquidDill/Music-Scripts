import os
import shutil
import hashlib
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

# Source and destination directories
source_dir = r'C:\Users\yanks\Music\All Music\Artists'
duplicates_dir = os.path.join(source_dir, 'Duplicates')

# Create the duplicates directory if it doesn't exist
os.makedirs(duplicates_dir, exist_ok=True)

def calculate_file_hash(file_path):
    """Calculate MD5 hash of the file."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
    except Exception as e:
        print(f'Error reading file {file_path}: {e}')
    return hasher.hexdigest()

def is_excluded_version(metadata):
    """Check if the file is a remix, acoustic, or re-release based on its metadata."""
    if metadata:
        title = metadata.get('title', [''])[0].lower()
        if 'remix' in title or 'acoustic' in title or 'version' in title or 're-release' in title:
            return True
    return False

def organize_duplicates(source):
    file_hashes = {}
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.lower().endswith(('.mp3', '.flac', '.ogg', '.m4a', '.wav', '.wma', '.aac')):
                try:
                    file_path = os.path.join(root, file)
                    file_hash = calculate_file_hash(file_path)
                    
                    audio = File(file_path, easy=True)
                    if audio is not None:
                        metadata = {
                            'title': audio.get('title', ['']),
                            'artist': audio.get('artist', ['']),
                            'album': audio.get('album', [''])
                        }
                    else:
                        metadata = None

                    if file_hash in file_hashes:
                        # Check if the file is a remix or a different version
                        if not is_excluded_version(metadata):
                            # Move the duplicate to the duplicates directory
                            duplicate_file_path = os.path.join(duplicates_dir, file)
                            if not os.path.exists(duplicate_file_path):
                                shutil.move(file_path, duplicate_file_path)
                                print(f'Moved duplicate: {file} to {duplicates_dir}')
                    else:
                        file_hashes[file_hash] = file_path

                except Exception as e:
                    print(f'Error processing file {file}: {e}')

# Run the function
organize_duplicates(source_dir)

