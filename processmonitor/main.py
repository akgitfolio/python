import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
import platform

console = Console()


def get_process_info():
    processes = []
    attrs = ["pid", "name", "cpu_percent", "memory_percent", "num_threads", "username"]
    if platform.system() != "Darwin":
        attrs.append("io_counters")

    for proc in psutil.process_iter(attrs):
        try:
            proc_info = proc.info
            if "io_counters" in proc_info:
                io_counters = proc_info["io_counters"]
                proc_info["read_bytes"] = io_counters.read_bytes
                proc_info["write_bytes"] = io_counters.write_bytes
            else:
                proc_info["read_bytes"] = 0
                proc_info["write_bytes"] = 0
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


def generate_table(processes):
    table = Table(title="Live Process Monitor")

    table.add_column("PID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("CPU %", justify="right", style="green")
    table.add_column("Memory %", justify="right", style="green")
    table.add_column("Read Bytes", justify="right", style="yellow")
    table.add_column("Write Bytes", justify="right", style="yellow")
    table.add_column("Threads", justify="right", style="blue")
    table.add_column("User", style="red")

    for proc in processes:
        table.add_row(
            str(proc["pid"]),
            proc["name"],
            f"{proc['cpu_percent']:.2f}",
            f"{proc['memory_percent']:.2f}",
            f"{proc['read_bytes']}",
            f"{proc['write_bytes']}",
            str(proc["num_threads"]),
            proc["username"],
        )

    return table


def main():
    with Live(console=console, refresh_per_second=1, screen=True) as live:
        while True:
            processes = get_process_info()

            processes = [p for p in processes if p["memory_percent"] is not None]
            processes.sort(key=lambda p: p["memory_percent"], reverse=True)
            table = generate_table(processes)
            live.update(table)
            time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
