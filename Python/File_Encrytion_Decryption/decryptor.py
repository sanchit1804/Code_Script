import sys
from utils import generate_key, decrypt_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python decryptor.py <encrypted_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    password = input("Enter password: ")

    with open(file_path, "rb") as f:
        file_data = f.read()

    # Extract salt and ciphertext
    salt = file_data[:16]
    ciphertext = file_data[16:]

    # Generate key from password + salt
    key, _ = generate_key(password, salt=salt)

    try:
        plaintext = decrypt_data(key, ciphertext)
    except Exception as e:
        print("Decryption failed! Wrong password or corrupted file.")
        sys.exit(1)

    # Save decrypted file
    if file_path.endswith(".enc"):
        out_file = file_path[:-4]
    else:
        out_file = file_path + ".dec"

    with open(out_file, "wb") as f:
        f.write(plaintext)

    print(f"File decrypted successfully: {out_file}")

if __name__ == "__main__":
    main()
