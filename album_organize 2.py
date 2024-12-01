import argparse
import os
import re
import shutil
from pathlib import Path

from mutagen import File, FileType, Tags
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis


parser = argparse.ArgumentParser(description='Organize music files by album within artist directories.')
parser.add_argument('-s', '--source-dir', type=str, help='Source directory containing music files', dest='source_dir', required=True)
parser.add_argument('-d', '--destination-dir', type=str, default=None, help='Optional destination directory for organized music files', dest='dest_dir', required=False)

args = parser.parse_args()

source_dir: Path = Path(args.source_dir)
dest_dir: Path = Path(args.dest_dir if args.dest_dir else source_dir)


if not source_dir.exists() or not source_dir.is_dir():
    raise NotADirectoryError(f"Source directory '{source_dir}' does not exist or is not a directory.")

if dest_dir and (not dest_dir.exists() or not dest_dir.is_dir()):
    raise NotADirectoryError(f"Destination directory '{dest_dir}' does not exist or is not a directory.")


SUPPORTED_EXTENSIONS: list[str] = ['.mp3', '.flac', '.ogg', '.m4a', '.wav', '.wma', '.aac']
UNKNOWN_ARTIST = 'Unknown Artist'
UNKNOWN_ALBUM = 'Unknown Album'


def sanitize_filename(name):
    """Remove or replace invalid characters for Windows filenames"""

    return re.sub(r'[<>:"/\\|?*]', '_', name)


def get_artist_and_album(audio: FileType):
    """Get the artist and album from the audio file tags"""
    
    match audio:
        case EasyID3() | FLAC() | OggVorbis():
            artist = audio.get('artist', UNKNOWN_ARTIST)
            album = audio.get('album', UNKNOWN_ALBUM)
        case _ if hasattr(audio, 'tags'):
            tags: Tags = audio.tags
            artist = tags.get('artist', UNKNOWN_ARTIST)
            album = tags.get('album', UNKNOWN_ALBUM)

    return sanitize_filename(artist), sanitize_filename(album)


def organize_music_by_album_within_artist(source):
    
    for root, _, files in os.walk(source):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                try:
                    file_path = os.path.join(root, file)
                    audio: FileType = File(file_path, easy=True)
                    
                    if audio is not None:
                        artist, album = get_artist_and_album(audio)
                    else:
                        artist = 'Unknown Artist'
                        album = 'Unknown Album'

                    # Check if the file is already in the correct artist directory
                    artist_dir = os.path.join(source, artist)
                    if not os.path.commonpath([file_path, artist_dir]) == artist_dir:
                        continue

                    # Create album directory within artist directory if it doesn't exist
                    album_dir = os.path.join(artist_dir, album)
                    os.makedirs(album_dir, exist_ok=True)

                    # Move the file to the album directory
                    shutil.move(file_path, os.path.join(album_dir, file))
                    print(f'Moved: {file} to {album_dir}')
                
                except Exception as e:
                    print(f'Error processing file {file}: {e}')


if __name__ == '__main__':
    organize_music_by_album_within_artist(source_dir)
