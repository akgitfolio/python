from cryptography.fernet import Fernet
import os
import json


class PasswordManager:
    def __init__(self, key_file="key.key", data_file="passwords.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.load_key()

    def load_key(self):
        if not os.path.exists(self.key_file):
            self.generate_key()
        with open(self.key_file, "rb") as key_file:
            self.key = key_file.read()

    def generate_key(self):
        self.key = Fernet.generate_key()
        with open(self.key_file, "wb") as key_file:
            key_file.write(self.key)

    def encrypt(self, data):
        fernet = Fernet(self.key)
        return fernet.encrypt(data.encode())

    def decrypt(self, encrypted_data):
        fernet = Fernet(self.key)
        return fernet.decrypt(encrypted_data).decode()

    def store_password(self, service, username, password):
        if not os.path.exists(self.data_file):
            data = {}
        else:
            with open(self.data_file, "rb") as file:
                data = self.decrypt(file.read())
                data = json.loads(data)
        data[service] = {"username": username, "password": self.encrypt(password)}
        with open(self.data_file, "wb") as file:
            file.write(self.encrypt(json.dumps(data)))

    def get_password(self, service):
        if not os.path.exists(self.data_file):
            return "Password manager is empty."
        with open(self.data_file, "rb") as file:
            data = self.decrypt(file.read())
            data = json.loads(data)
            if service in data:
                return f"Service: {service}\nUsername: {data[service]['username']}\nPassword: {self.decrypt(data[service]['password'])}"
            else:
                return f"No password found for service: {service}"


if __name__ == "__main__":
    password_manager = PasswordManager()

    password_manager.store_password("example.com", "user123", "password123")

    print(password_manager.get_password("example.com"))
