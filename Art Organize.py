import os

# List of common music file extensions
MUSIC_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a', '.alac'}

def identify_music_files(directory):
    music_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in MUSIC_EXTENSIONS:
                file_path = os.path.join(root, file)
                music_files.append(file_path)

    return music_files

if __name__ == "__main__":
    target_directory = r"C:\Users\yanks\Music\All Music\Art"
    music_files = identify_music_files(target_directory)

    if music_files:
        print("Music files found:")
        for file in music_files:
            print(file)
        print(f"\nTotal number of music files: {len(music_files)}")
    else:
        print("No music files found.")
