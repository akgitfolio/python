import secrets
import hashlib
import smtplib
import os
import base64
from cryptography.fernet import Fernet
from getpass import getpass

class PasswordManager:
    def __init__(self):
        self.passwords_folder = "passwords"
        if not os.path.exists(self.passwords_folder):
            os.makedirs(self.passwords_folder)

    def generate_password(self, website, category):
        base_password = secrets.token_urlsafe(16)
        website_hash = hashlib.sha256(website.encode()).hexdigest()[:8]
        category_hash = hashlib.sha256(category.encode()).hexdigest()[:4]
        return f"{base_password}-{website_hash}-{category_hash}"

    def send_verification_code(self, email, code):
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            message = f"Subject: Verification Code\n\nYour verification code is: {code}"
            server.sendmail(smtp_user, email, message)

    def store_password(self, website, username, password):
        master_password = getpass("Enter your master password: ")
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
        cipher = Fernet(base64.urlsafe_b64encode(key))
        encrypted_password = cipher.encrypt(password.encode())

        filename = os.path.join(self.passwords_folder, f"{website}_{username}.bin")
        with open(filename, 'wb') as f:
            f.write(salt + encrypted_password)

    def retrieve_password(self, website, username):
        master_password = getpass("Enter your master password: ")
        filename = os.path.join(self.passwords_folder, f"{website}_{username}.bin")
        try:
            with open(filename, 'rb') as f:
                data = f.read()
                salt = data[:16]
                encrypted_password = data[16:]
                key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)
                cipher = Fernet(base64.urlsafe_b64encode(key))
                password = cipher.decrypt(encrypted_password)
                return password.decode()
        except FileNotFoundError:
            print("Password not found!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def main_menu(self):
        while True:
            print("1. Generate Password")
            print("2. Store Password")
            print("3. Retrieve Password")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                website = input("Enter website name: ")
                category = input("Enter category (e.g., social media, banking): ")
                password = self.generate_password(website, category)
                print(f"Generated password: {password}")
            elif choice == '2':
                website = input("Enter website name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                email = input("Enter your email: ")
                verification_code = secrets.token_urlsafe(6)
                self.send_verification_code(email, verification_code)
                code = input("Enter verification code: ")
                if code == verification_code:
                    self.store_password(website, username, password)
                    print("Password stored successfully!")
                else:
                    print("Incorrect verification code!")
            elif choice == '3':
                website = input("Enter website name: ")
                username = input("Enter username: ")
                password = self.retrieve_password(website, username)
                if password:
                    print(f"Password: {password}")
            elif choice == '4':
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    password_manager = PasswordManager()
    password_manager.main_menu()
