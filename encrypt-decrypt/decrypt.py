from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64


def decrypt_file(encrypted_file, password):
    backend = default_backend()

    with open(encrypted_file, "rb") as f:
        salt = f.read(16)
        iv = f.read(12)
        encrypted_data = f.read()

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=backend)
    key = kdf.derive(password.encode())

    aesgcm = AESGCM(key)

    try:
        decrypted_data = aesgcm.decrypt(iv, encrypted_data, None)

        with open(encrypted_file[:-4], "wb") as f:
            f.write(decrypted_data)

        print(f"File '{encrypted_file}' decrypted successfully!")
    except Exception as e:
        print(f"Failed to decrypt file '{encrypted_file}': {e}")


if __name__ == "__main__":
    encrypted_file = input("Enter the path of the file to decrypt: ")
    password = input("Enter the password: ")
    decrypt_file(encrypted_file, password)
