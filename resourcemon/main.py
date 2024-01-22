import psutil
import pandas as pd
from datetime import datetime
import time
import logging


logging.basicConfig(
    filename="system_health_monitor.log",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


system_health_list = []


def log_system_health():
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_usage = psutil.disk_usage("/")

            system_health = {
                "timestamp": timestamp,
                "cpu_usage": cpu_usage,
                "memory_total": memory_info.total,
                "memory_used": memory_info.used,
                "memory_free": memory_info.free,
                "memory_percent": memory_info.percent,
                "disk_total": disk_usage.total,
                "disk_used": disk_usage.used,
                "disk_free": disk_usage.free,
                "disk_percent": disk_usage.percent,
            }

            system_health_list.append(system_health)
            logging.info(f"System health: {system_health}")

            print(system_health)

            time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping system health monitor and saving log...")
            save_log()
            break
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")


def save_log(filename="system_health_log.csv"):
    df = pd.DataFrame(system_health_list)
    df.to_csv(filename, index=False)
    print(f"Log saved to {filename}")
    logging.info(f"Log saved to {filename}")


if __name__ == "__main__":
    print("Starting system health monitor...")
    logging.info("Starting system health monitor")
    log_system_health()
