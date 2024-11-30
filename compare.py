import os

def get_all_files(directory):
    """
    Recursively fetch all files in a directory, including their relative paths.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            file_list.append(relative_path)
    return set(file_list)

def compare_directories(dir1, dir2, output_file):
    """
    Compare two directories and output the differences to a text file.
    """
    # Get all files in both directories
    dir1_files = get_all_files(dir1)
    dir2_files = get_all_files(dir2)

    # Find differences
    only_in_dir1 = dir1_files - dir2_files
    only_in_dir2 = dir2_files - dir1_files

    # Write differences to the output file using UTF-8 encoding
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Differences between:\n{dir1}\nand\n{dir2}\n\n")
        f.write("Files only in the first directory:\n")
        for file in sorted(only_in_dir1):
            f.write(f"{file}\n")

        f.write("\nFiles only in the second directory:\n")
        for file in sorted(only_in_dir2):
            f.write(f"{file}\n")

    print(f"Differences have been written to {output_file}")

if __name__ == "__main__":
    # Directories to compare
    directory1 = r"C:\Users\yanks\Music\iTunes\iTunes Media\Music"
    directory2 = r"C:\Users\yanks\OneDrive\Desktop\iTunes Media\Music"

    # Output file
    output_file = r"C:\Users\yanks\OneDrive\Documents\directory_differences.txt"

    # Perform comparison
    compare_directories(directory1, directory2, output_file)
