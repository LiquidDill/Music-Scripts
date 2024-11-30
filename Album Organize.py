import os

def create_symlinks(source_directory, target_directory, verbose=False):
    if verbose:
        print(f"Source directory: {source_directory}")
        print(f"Target directory: {target_directory}")
    
    if not os.path.exists(source_directory):
        print(f"Error: Source directory does not exist: {source_directory}")
        return
    
    if not os.path.exists(target_directory):
        print(f"Error: Target directory does not exist: {target_directory}")
        return
    
    for artist in os.listdir(source_directory):
        artist_path = os.path.join(source_directory, artist)
        if os.path.isdir(artist_path):
            for album in os.listdir(artist_path):
                album_path = os.path.join(artist_path, album)
                if os.path.isdir(album_path):
                    target_album_path = os.path.join(target_directory, album)
                    
                    if not os.path.exists(target_album_path):
                        os.makedirs(target_album_path)
                        if verbose:
                            print(f"Created directory: {target_album_path}")
                    
                    for file in os.listdir(album_path):
                        file_path = os.path.join(album_path, file)
                        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                            symlink_path = os.path.join(target_album_path, file)
                            if not os.path.exists(symlink_path):
                                try:
                                    os.symlink(file_path, symlink_path)
                                    if verbose:
                                        print(f"Created symlink for {file} at {symlink_path}")
                                except Exception as e:
                                    print(f"Error creating symlink for {file} at {symlink_path}: {e}")
                            else:
                                if verbose:
                                    print(f"Symlink already exists for {file} at {symlink_path}")
        else:
            if verbose:
                print(f"Skipping non-directory: {artist_path}")

if __name__ == "__main__":
    source_directory = r"C:\Users\yanks\Music\All Music\Art"
    target_directory = r"C:\Users\yanks\Music\All Music\Albums"
    create_symlinks(source_directory, target_directory, verbose=True)
