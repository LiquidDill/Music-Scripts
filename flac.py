import os

def is_wma(file_path):
    # This function assumes files with .wma extension are WMA files.
    # For more advanced detection, you'd need specific libraries or tools.
    return file_path.lower().endswith('.wma')

def list_wma_files(directory):
    wma_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_wma(file_path):
                wma_files.append(file_path)
    return wma_files

def save_to_file(wma_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Total WMA files: {len(wma_files)}\n\n")
        for wma_file in wma_files:
            f.write(f"{wma_file}\n")

music_directory = r'C:\Users\yanks\Music\All Music\Artists'
output_file = r'C:\Users\yanks\OneDrive\Documents\wma_files_list.txt'

wma_files = list_wma_files(music_directory)
save_to_file(wma_files, output_file)

print(f"List of WMA files saved to {output_file}")
