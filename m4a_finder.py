import os

def find_m4a_files(directory, output_file):
    """
    Recursively find all .m4a files in the specified directory and write them to an output file.
    """
    m4a_files = []

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.m4a'):  # Check if the file has a .m4a extension
                m4a_files.append(os.path.join(root, file))

    # Write the list of .m4a files to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("List of .m4a files found:\n")
        f.write("\n".join(m4a_files))
    
    print(f"Found {len(m4a_files)} .m4a files. List saved to {output_file}")

if __name__ == "__main__":
    # Directory to search
    search_directory = r"C:\Users\yanks\OneDrive\Desktop\iTunes Media\Music"
    
    # Output file
    output_file_path = r"C:\Users\yanks\OneDrive\Documents\m4a_files_list.txt"

    # Find and list .m4a files
    find_m4a_files(search_directory, output_file_path)
