import time

LOG_FILE = "logs.txt"


def collect_logs():
    with open(LOG_FILE, "a") as f:
        while True:
            log_message = generate_log()
            timestamp = int(time.time())
            f.write(f"{timestamp}: {log_message}\n")
            time.sleep(1)


if __name__ == "__main__":
    print("Log Aggregator started. Logs are being collected...")
    collect_logs()
