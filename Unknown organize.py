import os
import shutil
from mutagen.easyid3 import EasyID3

# Define paths
source_dir = r'H:\Music\Unknown Artist'
destination_base_dir = r'H:\Music'

# Ensure source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory {source_dir} does not exist.")
    exit()

# Loop through each file in the source directory
for filename in os.listdir(source_dir):
    if not filename.endswith((".mp3", ".flac", ".m4a")):  # Check for audio file types
        continue

    # Define the source file path
    source_file = os.path.join(source_dir, filename)

    try:
        # Load the audio file's metadata
        audio = EasyID3(source_file)
        artist_name = audio.get('artist', ['Unknown Artist'])[0].strip()
    except Exception as e:
        print(f"Could not read metadata for {filename}: {e}")
        continue

    # Define the destination directory based on the artist name
    destination_dir = os.path.join(destination_base_dir, artist_name)

    # Create the artist directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Define the destination file path
    destination_file = os.path.join(destination_dir, filename)

    # Move the file
    try:
        shutil.move(source_file, destination_file)
        print(f'Moved: {filename} to {destination_dir}')
    except Exception as e:
        print(f"Failed to move {filename}: {e}")

print("Files have been moved successfully!")
