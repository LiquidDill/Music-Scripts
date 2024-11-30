from mutagen.flac import FLAC, Picture
from mutagen.id3 import APIC, ID3, PictureType, ID3NoHeaderError 
import os
import subprocess
import sys
import time

num_files = 0

# https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list
def run_fast_scandir(dir, ext):
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            file_ext = os.path.splitext(f.name)[1].lower()
            if file_ext in ext:
                if file_ext == '.mp3':
                    fix_mp3(f.path)
                elif file_ext == '.flac':
                    fix_flac(f.path)
                elif file_ext == '.jpg':
                    fix_jpg(f.path)
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files

def fix_mp3(file):
    try:
        tag = ID3(file)
    except ID3NoHeaderError:
        return
    if len(tag.getall("APIC")) > 0:
        print(file)
        with open("temp.jpg", "wb") as f:
            f.write(tag.getall("APIC")[0].data)
        subprocess.run(['magick', '-interlace', 'None', 'temp.jpg', 'temp.jpg'])
        tag.delall("APIC")
        with open("temp.jpg", 'rb') as f:
            tag.add(APIC(3, 'image/jpeg', 3, u'cover', data=f.read()))
        tag.save()
        global num_files
        num_files += 1

def fix_flac(file):
    tag = FLAC(file)
    pics = tag.pictures
    for p in pics:
        if p.type == 3:
            print(file)
            with open("temp.jpg", "wb") as f:
                f.write(p.data)
            subprocess.run(['magick', '-interlace', 'None', 'temp.jpg', 'temp.jpg'])
            tag.clear_pictures()
            image = Picture()
            image.type = PictureType.COVER_FRONT
            image.mime = 'image/jpeg'
            with open('temp.jpg', 'rb') as f:
                image.data = f.read()
            tag.add_picture(image)
            tag.save(deleteid3=True)
            global num_files
            num_files += 1

def fix_jpg(file):
    print(file)
    subprocess.run(['magick', '-interlace', 'None', file, file])
    global num_files
    num_files += 1


def timer(start,end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)


if len(sys.argv) > 1:
    start = time.time()
    subfolders, files = run_fast_scandir(sys.argv[1].replace("\\", "/"), {".flac", ".mp3", ".jpg"})
    end = time.time()
    print("\n" + str(num_files) + " files processed in " + timer(start, end))
else:
    print("You must provide a path between quotes. For example: python fix_albumart.py \"R:\\My Music\"")
