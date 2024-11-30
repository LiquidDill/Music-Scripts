import os
import requests

# Last.fm API key
LASTFM_API_KEY = "7ec49f29e359cb7c7311177cc2573279"  # Replace with your Last.fm API key

# Path to the local default image
DEFAULT_IMAGE_PATH = r"C:\path\to\default_image.jpg"  # Replace with your local file path

def fetch_album_art(album_name, artist_name):
    try:
        url = (
            f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo"
            f"&api_key={LASTFM_API_KEY}&artist={artist_name}&album={album_name}&format=json"
        )
        response = requests.get(url)
        data = response.json()
        if 'album' in data and 'image' in data['album']:
            images = data['album']['image']
            for image in images:
                if image['size'] == 'extralarge':
                    return requests.get(image['#text']).content
    except Exception as e:
        print(f"Error fetching album art: {e}")
    return None

def fetch_default_image():
    if os.path.exists(DEFAULT_IMAGE_PATH):
        with open(DEFAULT_IMAGE_PATH, 'rb') as file:
            return file.read()
    else:
        print(f"Default image not found at: {DEFAULT_IMAGE_PATH}")
    return None

def save_album_art(directory, album_art):
    file_path = os.path.join(directory, "album_art.jpg")
    with open(file_path, 'wb') as file:
        file.write(album_art)

def process_directory(base_directory):
    for artist in os.listdir(base_directory):
        artist_path = os.path.join(base_directory, artist)
        if os.path.isdir(artist_path):
            for album in os.listdir(artist_path):
                album_path = os.path.join(artist_path, album)
                if os.path.isdir(album_path):
                    print(f"Processing album: {album}")
                    album_art = fetch_album_art(album, artist)
                    if album_art:
                        save_album_art(album_path, album_art)
                        print(f"Saved album art for {album} to {album_path}")
                    else:
                        print(f"No album art found for {album}, using default image")
                        default_image = fetch_default_image()
                        if default_image:
                            save_album_art(album_path, default_image)
                        else:
                            print(f"Failed to fetch default image for {album}")

if __name__ == "__main__":
    music_directory = r"C:\Users\yanks\Music\All Music\Artists"
    process_directory(music_directory)
