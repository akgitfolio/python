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


def encrypt_file(input_file, password):
    backend = default_backend()
    salt = os.urandom(16)
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=backend)
    key = kdf.derive(password.encode())

    iv = os.urandom(12)
    aesgcm = AESGCM(key)

    with open(input_file, "rb") as f:
        data = f.read()

    encrypted_data = aesgcm.encrypt(iv, data, None)

    with open(input_file + ".enc", "wb") as f:
        f.write(salt + iv + encrypted_data)

    print(f"File '{input_file}' encrypted successfully!")


if __name__ == "__main__":
    input_file = input("Enter the path of the file to encrypt: ")
    password = input("Enter the password: ")
    encrypt_file(input_file, password)
