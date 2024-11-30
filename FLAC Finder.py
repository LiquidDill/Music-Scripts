import os
import shutil

# Hard-coded source and target directories
source_directory = r"C:\Users\yanks\Music\iTunes\iTunes Media"
target_directory = r"C:\Users\yanks\OneDrive\Desktop\FLAC Files"

def move_flac_files(source, target):
    """Move all .flac files from the source directory to the target directory."""
    try:
        # Create the target directory if it doesn't exist
        if not os.path.exists(target):
            os.makedirs(target)
            print(f"Created target directory: {target}")
        
        flac_files_moved = 0

        # Walk through the source directory to find .flac files
        for root, _, files in os.walk(source):
            for file in files:
                if file.lower().endswith(".flac"):  # Check for .flac extension (case-insensitive)
                    source_file_path = os.path.join(root, file)
                    target_file_path = os.path.join(target, file)

                    # Move the file
                    try:
                        shutil.move(source_file_path, target_file_path)
                        flac_files_moved += 1
                        print(f"Moved: {source_file_path} -> {target_file_path}")
                    except Exception as e:
                        print(f"Error moving file {source_file_path}: {e}")
        
        if flac_files_moved == 0:
            print("No FLAC files found to move.")
        else:
            print(f"Successfully moved {flac_files_moved} FLAC files to {target}")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """Main function to execute the FLAC file mover."""
    print(f"Moving FLAC files from '{source_directory}' to '{target_directory}'...")
    move_flac_files(source_directory, target_directory)
    print("Operation completed.")

if __name__ == "__main__":
    main()
