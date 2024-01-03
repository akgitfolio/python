import platform
import psutil
import socket


def get_system_information():
    system_info = {}

    system_info["System"] = platform.system()
    system_info["Node Name"] = platform.node()
    system_info["Release"] = platform.release()
    system_info["Version"] = platform.version()
    system_info["Machine"] = platform.machine()
    system_info["Processor"] = platform.processor()

    system_info["CPU Cores"] = psutil.cpu_count(logical=False)
    system_info["CPU Threads"] = psutil.cpu_count(logical=True)
    system_info["CPU Usage (%)"] = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    system_info["Total Memory (GB)"] = round(mem.total / (1024**3), 2)
    system_info["Available Memory (GB)"] = round(mem.available / (1024**3), 2)
    system_info["Memory Usage (%)"] = mem.percent

    partitions = psutil.disk_partitions()
    for partition in partitions:
        mount_point = partition.mountpoint
        disk_usage = psutil.disk_usage(mount_point)
        system_info[f"Disk Usage {mount_point} (GB)"] = round(
            disk_usage.used / (1024**3), 2
        )
        system_info[f"Disk Total {mount_point} (GB)"] = round(
            disk_usage.total / (1024**3), 2
        )

    system_info["Hostname"] = socket.gethostname()
    system_info["IP Address"] = socket.gethostbyname(socket.gethostname())

    return system_info


def display_system_information(system_info):
    print("\nSystem Information:\n")
    for key, value in system_info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    system_info = get_system_information()
    display_system_information(system_info)
