import os
import time
import requests
from mutagen.id3 import ID3, APIC
from musicbrainzngs import set_useragent, search_releases

# Set up MusicBrainz user agent
set_useragent('AlbumArtFetcher', '1.0')

def fetch_album_art(artist, album):
    print(f"Fetching album art for artist: {artist}, album: {album}")
    try:
        result = search_releases(artist=artist, release=album, limit=1)
        if result['release-list']:
            cover_art_url = result['release-list'][0]['cover-art-archive']['front']
            if cover_art_url:
                print(f"Cover art URL found: {cover_art_url}")
                response = requests.get(cover_art_url)
                return response.content
            else:
                print("No cover art URL found in the response.")
        else:
            print("No release found in the response.")
    except Exception as e:
        print(f"Error fetching album art: {e}")
    return None

def apply_album_art(file_path, art_data):
    print(f"Applying album art to file: {file_path}")
    try:
        audio_file = ID3(file_path)
        audio_file.delall("APIC")
        audio_file.add(APIC(encoding=3, mime='image/jpeg', type=3, data=art_data))
        audio_file.save()
        print(f"Album art applied successfully.")
    except Exception as e:
        print(f"Error applying album art: {e}")

def process_directory(directory):
    files = [f for f in os.listdir(directory) if f.lower().endswith('.mp3')]
    total_files = len(files)
    start_time = time.time()

    for i, filename in enumerate(files, start=1):
        file_path = os.path.join(directory, filename)
        print(f"Processing file {i}/{total_files}: {filename}")
        try:
            audio_file = ID3(file_path)
            artist = audio_file.get('TPE1', 'Unknown Artist').text[0]
            album = audio_file.get('TALB', 'Unknown Album').text[0]
            print(f"Artist: {artist}, Album: {album}")
            art_data = fetch_album_art(artist, album)
            if art_data:
                apply_album_art(file_path, art_data)
                print(f"Album art updated for {filename}")
            else:
                print(f"No album art found for {filename}")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

        # Update status bar
        elapsed_time = time.time() - start_time
        estimated_total_time = (elapsed_time / i) * total_files
        eta = estimated_total_time - elapsed_time
        status_bar = f"Progress: {i}/{total_files} files processed. ETA: {eta:.2f} seconds"
        print(status_bar, end='\r')

    print("\nProcessing complete.")

# Set the directory you want to process
directory_path = r'C:\Users\yanks\Music\All Music\Artists'
process_directory(directory_path)
