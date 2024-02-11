import time
import random

LOG_LEVELS = ["INFO", "DEBUG", "WARNING", "ERROR"]
CATEGORIES = ["Authentication", "Database", "Network", "Security"]
SERVICES = ["Service A", "Service B", "Service C"]


def generate_log():
    timestamp = int(time.time())
    log_level = random.choice(LOG_LEVELS)
    category = random.choice(CATEGORIES)
    service = random.choice(SERVICES)
    response_time = round(random.uniform(0.1, 5), 2)
    status_code = random.choice([200, 404, 500])
    message = f"[{service}] [{category}] {log_level} - Response Time: {response_time}s, Status Code: {status_code}"
    return message


if __name__ == "__main__":
    while True:
        log_message = generate_log()
        print(log_message)
        time.sleep(random.randint(1, 5))
