import shutil
import os
import zipfile
import datetime


class BackupManager:
    def __init__(self, backup_folder):
        self.backup_folder = backup_folder

    def create_backup(self, files_to_backup):
        backup_name = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        backup_path = os.path.join(self.backup_folder, backup_name)

        try:
            with zipfile.ZipFile(backup_path, "w") as zipf:
                for file_to_backup in files_to_backup:
                    if os.path.isfile(file_to_backup):
                        zipf.write(file_to_backup, os.path.basename(file_to_backup))
                    elif os.path.isdir(file_to_backup):
                        for root, _, files in os.walk(file_to_backup):
                            for file in files:
                                file_path = os.path.join(root, file)
                                zipf.write(
                                    file_path,
                                    os.path.relpath(file_path, file_to_backup),
                                )
                    else:
                        print(
                            f"Warning: {file_to_backup} is neither a file nor a directory. Skipping."
                        )
            print(f"Backup created successfully: {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")

    def restore_backup(self, backup_file, restore_location):
        try:
            with zipfile.ZipFile(backup_file, "r") as zipf:
                zipf.extractall(restore_location)
            print(f"Backup restored successfully to: {restore_location}")
        except Exception as e:
            print(f"Error restoring backup: {e}")


if __name__ == "__main__":
    backup_folder = "backups"
    files_to_backup = ["file1.txt", "directory_to_backup"]
    backup_file = "backup_20240102_120000.zip"
    restore_location = "restored_files"

    backup_manager = BackupManager(backup_folder)
    backup_manager.create_backup(files_to_backup)
    backup_manager.restore_backup(backup_file, restore_location)
