import os
import shutil
import re
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from PIL import Image

# Source and destination directories
cover_source_dir = r'C:\Users\yanks\Music\Rips'
music_dest_dir = r'C:\Users\yanks\Music\All Music\Artists'

def sanitize_filename(name):
    # Remove or replace invalid characters for Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def get_artist_and_album_from_audio(file_path):
    audio = File(file_path, easy=True)
    if audio is None:
        return 'Unknown Artist', 'Unknown Album'
    
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

def move_album_covers(source, destination):
    supported_image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    for root, dirs, files in os.walk(source):
        for file in files:
            if file.lower().endswith(supported_image_extensions):
                try:
                    file_path = os.path.join(root, file)

                    # Assuming the album cover files are named with artist and album information
                    # Example filename: "Artist - Album Cover.jpg"
                    base_name = os.path.splitext(file)[0]
                    parts = base_name.split(' - ')
                    if len(parts) >= 2:
                        artist = sanitize_filename(parts[0])
                        album = sanitize_filename(parts[1])
                    else:
                        # If filename does not contain artist and album, try to read metadata from an audio file
                        artist, album = get_artist_and_album_from_audio(file_path)

                    # Create artist and album directories if they don't exist
                    artist_dir = os.path.join(destination, artist)
                    album_dir = os.path.join(artist_dir, album)
                    if not os.path.exists(album_dir):
                        print(f"Album directory for {artist} - {album} not found. Skipping file: {file}")
                        continue
                    
                    # Move the album cover to the album directory
                    shutil.move(file_path, os.path.join(album_dir, file))
                    print(f'Moved: {file} to {album_dir}')
                
                except Exception as e:
                    print(f'Error processing file {file}: {e}')

# Run the function
move_album_covers(cover_source_dir, music_dest_dir)
