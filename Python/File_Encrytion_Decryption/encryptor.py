import sys
from utils import generate_key, encrypt_data
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python encryptor.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    password = input("Enter password: ")

    # Read file
    with open(file_path, "rb") as f:
        data = f.read()

    # Generate key
    key, salt = generate_key(password)

    # Encrypt
    ciphertext = encrypt_data(key, data)

    # Save encrypted file (prepend salt)
    out_file = file_path + ".enc"
    with open(out_file, "wb") as f:
        f.write(salt + ciphertext)

    print(f"File encrypted successfully: {out_file}")

if __name__ == "__main__":
    main()
