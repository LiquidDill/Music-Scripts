import os

# Directory to scan for music files
music_dir = r'C:\Users\yanks\Music\All Music'

# Common audio file extensions
audio_extensions = ('.mp3', '.flac', '.ogg', '.m4a', '.wav', '.wma', '.aac')

def count_songs(directory):
    song_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(audio_extensions):
                song_count += 1
    return song_count

def main():
    total_songs = count_songs(music_dir)
    print(f'Total number of songs in "{music_dir}": {total_songs}')

if __name__ == "__main__":
    main()
