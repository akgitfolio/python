import platform
import psutil
import time


def list_disks(primary_disk):
    disks = []
    if platform.system() == "Windows":
        for partition in psutil.disk_partitions():
            if "cdrom" not in partition.opts and partition.fstype != "":
                label = "(Primary)" if partition.device == primary_disk else ""
                disks.append((partition.device, label))
    else:
        partitions = psutil.disk_partitions(all=True)
        for partition in partitions:
            if partition.device not in disks:
                label = "(Primary)" if partition.mountpoint == "/" else ""
                disks.append((partition.device, label))
    return disks


def select_disk(disks):
    print("Available disks:")
    for i, (disk, label) in enumerate(disks):
        print(f"{i+1}. {disk} {label}")
    while True:
        choice = input("Enter the number of the disk you want to monitor: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(disks):
                return disks[choice - 1][0]
            else:
                print("Invalid input. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def monitor_disk(disk):

    THRESHOLD_PERCENT = 90

    while True:

        usage = psutil.disk_usage(disk)
        disk_percent = usage.percent

        if disk_percent > THRESHOLD_PERCENT:

            print(f"Disk usage on {disk} exceeds {THRESHOLD_PERCENT}%!")

        else:
            print(f"Disk usage on {disk} is below {THRESHOLD_PERCENT}%.")

        time.sleep(300)


if __name__ == "__main__":
    if platform.system() == "Windows":
        primary_disk = psutil.disk_partitions()[0].device
    else:
        primary_disk = "/"
    disks = list_disks(primary_disk)
    if not disks:
        print("No disks found.")
    else:
        selected_disk = select_disk(disks)
        print(f"Monitoring disk: {selected_disk}")
        monitor_disk(selected_disk)
