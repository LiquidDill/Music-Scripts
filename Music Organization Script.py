import os
import shutil
import re
from mutagen.easyid3 import EasyID3  # This library helps to read metadata from MP3 files

# Define paths
source_dir = r"H:\Music\Unknown Artist"
target_dir = r"H:\Music"

# Function to clean and extract the primary artist's name
def get_primary_artist(artist_name):
    # Regular expression to match variations of "feat", "ft", etc., and commas
    split_patterns = re.compile(r'(,| feat\.? | ft\.? | featuring )', re.IGNORECASE)
    
    # Split the artist name at the first occurrence of the pattern
    primary_artist = re.split(split_patterns, artist_name)[0]
    
    return primary_artist.strip()

# Function to move files
def move_music_files():
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(('.mp3', '.flac', '.wav')):  # Add more extensions if needed
                file_path = os.path.join(root, file)
                
                try:
                    # Extract metadata
                    audio = EasyID3(file_path)
                    
                    # Check for artist in different tags
                    artist = (
                        audio.get('artist') or 
                        audio.get('performer') or 
                        audio.get('composer')
                    )
                    
                    if artist:
                        # Get primary artist name
                        artist_name = get_primary_artist(artist[0])
                        # Determine destination folder
                        dest_folder = os.path.join(target_dir, artist_name)

                        # Create the folder if it doesn't exist
                        if not os.path.exists(dest_folder):
                            os.makedirs(dest_folder)
                            print(f"Created directory: {dest_folder}")
                        
                        # Move the file
                        shutil.move(file_path, dest_folder)
                        print(f"Moved {file} to {dest_folder}")

                    else:
                        print(f"No artist metadata found for {file}. Skipping...")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    move_music_files()
