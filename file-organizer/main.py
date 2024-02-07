import os
import shutil
import exifread

source_folder = "/path/to/source/folder"
destination_folder = "/path/to/destination/folder"
file_types = [".jpg", ".png", ".tiff"]
organization_rules = {
    "by_date": True,
    "by_camera_model": True,
    "by_tag": ["portrait", "landscape"],
}

def extract_metadata(image_path):
    with open(image_path, "rb") as f:
        tags = exifread.process_file(f)
        return {
            "camera_model": tags.get("Image Model", "Unknown Camera"),
            "date_taken": tags.get("EXIF DateTimeOriginal", "Unknown Date"),
            "location": tags.get("GPS GPSLatitude", "Unknown Location"),
        }

def create_target_path(metadata, organization_rules):
    path_elements = []
    
    if organization_rules.get("by_date") and metadata["date_taken"] != "Unknown Date":
        date_taken = str(metadata["date_taken"]).split()[0].replace(":", "-")
        path_elements.append(date_taken)
    
    if organization_rules.get("by_camera_model") and metadata["camera_model"] != "Unknown Camera":
        path_elements.append(str(metadata["camera_model"]))
    
    if organization_rules.get("by_tag"):
        for tag in organization_rules["by_tag"]:
            if tag in metadata.get("tags", []):
                path_elements.append(tag)
    
    return os.path.join(*path_elements)

def organize_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(tuple(file_types)):
            file_path = os.path.join(source_folder, filename)
            metadata = extract_metadata(file_path)
            target_subfolder = create_target_path(metadata, organization_rules)
            target_path = os.path.join(destination_folder, target_subfolder)

            if not os.path.exists(target_path):
                os.makedirs(target_path)

            shutil.move(file_path, os.path.join(target_path, filename))

organize_files(source_folder, destination_folder)
