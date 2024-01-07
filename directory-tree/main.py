import os
import shutil
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

class DirectoryTreeGenerator:
    def __init__(self, target_folder):
        self.target_folder = target_folder

    def add_file(self, filename, key):
        directory_path = os.path.join(self.target_folder, key)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        
        shutil.move(filename, os.path.join(directory_path, os.path.basename(filename)))

    def generate(self):
        pass

def generate_music_library(music_folder, target_folder, organization_level="album_artist"):
    tree_generator = DirectoryTreeGenerator(target_folder)

    for filename in os.listdir(music_folder):
        filepath = os.path.join(music_folder, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            audio = MP3(filepath, ID3=EasyID3)
            artist = audio.get("artist", ["Unknown Artist"])[0]
            album = audio.get("album", ["Unknown Album"])[0]

            if organization_level == "artist":
                key = artist
            elif organization_level == "album_artist":
                key = os.path.join(artist, album)
            else:
                key = "Unknown"

            tree_generator.add_file(filepath, key)
        except Exception as e:
            print(f"Error processing file: {filename}. Skipping...")
            print(f"Error message: {e}")

    tree_generator.generate()

if __name__ == "__main__":
    music_folder = "/path/to/your/music/collection"
    target_folder = "/path/to/organized/music/library"
    organization_level = "album_artist"

    generate_music_library(music_folder, target_folder, organization_level)
