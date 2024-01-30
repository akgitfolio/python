import requests
import json
import time
import random
from faker import Faker


BASE_URL = "http://127.0.0.1:5000"
NUM_ITERATIONS = 100
DELAY = 2


fake = Faker()


def register_user(username, password):
    url = f"{BASE_URL}/register"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print(f"Register response: {response.status_code}, {response.json()}")
    return response.status_code == 201


def login_user(username, password):
    url = f"{BASE_URL}/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    print(f"Login response: {response.status_code}, {response.json()}")
    return response.status_code == 200


def simulate_logins(iterations, delay):
    for i in range(iterations):
        print(f"Iteration {i + 1}/{iterations}")

        username = fake.user_name()
        password = fake.password()

        if register_user(username, password):

            if random.choice([True, False]):
                print("Simulating successful login...")
                login_user(username, password)
            else:
                print("Simulating failed login...")
                login_user(username, "wrongpassword")

        time.sleep(delay)


if __name__ == "__main__":
    simulate_logins(NUM_ITERATIONS, DELAY)
