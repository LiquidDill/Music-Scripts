import os
import shutil
import re
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis

# Source and destination directories
source_dir = r'C:\Users\yanks\Music\All Music\Artists'
music_dest_dir = source_dir  # Destination is the same as the source

def sanitize_filename(name):
    # Remove or replace invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def extract_main_artist(artist_name):
    # Extract the main artist from a featured artist name
    # This assumes the format "Artist feat. FeaturedArtist" or "Artist ft. FeaturedArtist"
    if 'feat' in artist_name.lower():
        return artist_name.split('feat')[0].strip()
    elif 'ft' in artist_name.lower():
        return artist_name.split('ft')[0].strip()
    else:
        return artist_name

def get_artist_and_album(audio):
    artist = 'Unknown Artist'
    album = 'Unknown Album'
    
    if isinstance(audio, EasyID3):
        artist = audio.get('artist', [artist])[0]
        album = audio.get('album', [album])[0]
    elif isinstance(audio, FLAC):
        artist = audio.get('artist', [artist])[0]
        album = audio.get('album', [album])[0]
    elif isinstance(audio, OggVorbis):
        artist = audio.get('artist', [artist])[0]
        album = audio.get('album', [album])[0]
    elif audio.tags:  # Catch-all for other types with tags
        artist = audio.tags.get('artist', [artist])[0]
        album = audio.tags.get('album', [album])[0]

    return sanitize_filename(artist), sanitize_filename(album)

def organize_featured_artists(source, destination):
    supported_extensions = ('.mp3', '.flac', '.ogg', '.m4a', '.wav', '.wma', '.aac')
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.lower().endswith(supported_extensions):
                try:
                    file_path = os.path.join(root, file)
                    audio = File(file_path, easy=True)
                    
                    if audio is not None:
                        artist, album = get_artist_and_album(audio)
                        main_artist = extract_main_artist(artist)
                    else:
                        artist = 'Unknown Artist'
                        album = 'Unknown Album'
                        main_artist = extract_main_artist(artist)

                    # Create artist directory if it doesn't exist
                    artist_dir = os.path.join(destination, main_artist)
                    os.makedirs(artist_dir, exist_ok=True)

                    # Create album directory within artist directory if it doesn't exist
                    album_dir = os.path.join(artist_dir, album)
                    os.makedirs(album_dir, exist_ok=True)

                    # Move the file to the album directory
                    shutil.move(file_path, os.path.join(album_dir, file))
                    print(f'Moved: {file} to {album_dir}')
                
                except Exception as e:
                    print(f'Error processing file {file}: {e}')

# Run the function
organize_featured_artists(source_dir, music_dest_dir)
