import datetime
import os
import platform
import psutil
import shutil
import subprocess
import socket
import json
import logging
import getpass


def adjust_system_date():
    new_date = datetime.datetime(2024, 6, 2)
    if platform.system() == "Windows":
        os.system(f"date {new_date.strftime('%m-%d-%Y')}")
    elif platform.system() == "Linux":
        os.system(f"date -s '{new_date.strftime('%Y-%m-%d %H:%M:%S')}'")
    elif platform.system() == "Darwin":
        os.system(f"date {new_date.strftime('%m%d%H%M%Y')}")


def modify_environment_variable():
    if platform.system() == "Windows":
        os.environ["PATH"] += ";C:\\New\\Path\\Directory"
    else:
        os.environ["PATH"] += ":/new/path/directory"


def modify_network_configuration():
    if platform.system() == "Windows":
        os.system("netsh interface ipv4 set dns 'Local Area Connection' static 8.8.8.8")
    elif platform.system() == "Linux":
        os.system("nmcli con mod 'Wired connection 1' ipv4.dns 8.8.8.8")
    elif platform.system() == "Darwin":
        os.system("networksetup -setdnsservers Wi-Fi 8.8.8.8")


def get_system_information():
    system_info = {}

    system_info["Platform"] = platform.platform()
    system_info["Processor"] = platform.processor()
    system_info["Memory"] = psutil.virtual_memory().total

    return system_info


def organize_files(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1][1:].lower()
            file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            date_folder = file_mod_time.strftime("%Y-%m-%d")
            type_folder = file_extension if file_extension else "unknown"

            dest_folder = os.path.join(destination_dir, type_folder, date_folder)
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)

            shutil.move(file_path, os.path.join(dest_folder, filename))


def manage_processes():

    for proc in psutil.process_iter(["pid", "name", "username"]):
        print(proc.info)


def manage_users():
    if platform.system() == "Windows":

        os.system("net user newuser password /add")
    else:

        os.system("sudo adduser newuser")


def manage_services():
    if platform.system() == "Windows":

        os.system("net start ServiceName")
    else:

        os.system("sudo systemctl start servicename")


def perform_network_operations():

    hostname = "google.com"
    response = os.system(f"ping -c 1 {hostname}")
    if response == 0:
        print(f"{hostname} is reachable")
    else:
        print(f"{hostname} is not reachable")

    if platform.system() == "Windows":
        os.system(f"tracert {hostname}")
    else:
        os.system(f"traceroute {hostname}")


def backup_system():
    source_dir = "/path/to/source"
    backup_dir = "/path/to/backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    shutil.copytree(source_dir, backup_dir)


def monitor_system():

    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage: {cpu_usage}%")

    memory_info = psutil.virtual_memory()
    print(f"Memory Usage: {memory_info.percent}%")


def log_system_events():
    logging.basicConfig(filename="system_events.log", level=logging.INFO)
    logging.info("System event logged")


def enhance_security():

    if platform.system() == "Windows":
        os.system("net user newuser newpassword")
    else:
        os.system("echo 'newuser:newpassword' | sudo chpasswd")


def main():
    adjust_system_date()
    modify_environment_variable()
    modify_network_configuration()

    system_info = get_system_information()
    logging.info("System Information: %s", json.dumps(system_info, indent=4))

    organize_files("source_dir", "destination_dir")
    manage_processes()
    manage_users()
    manage_services()
    perform_network_operations()
    backup_system()
    monitor_system()
    log_system_events()
    enhance_security()


if __name__ == "__main__":
    main()
