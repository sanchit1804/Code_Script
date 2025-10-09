
# File_Encryption_Decryption

A simple **AES-based file encryption and decryption module** in Python with **password-based key generation**.
Supports encrypting and decrypting any file using a password entered from the command line.

---

## **Features**

* AES encryption (CFB mode)
* Password-based key derivation (PBKDF2HMAC + SHA256)
* Modular code: `utils.py` handles encryption/decryption logic
* CLI-based usage for files
* Supports any file type (images, documents, etc.)

---

## **File Structure**

```
File_Encryption_Decryption/
├── encryptor.py        # CLI tool to encrypt files
├── decryptor.py        # CLI tool to decrypt files
├── utils.py            # Encryption/decryption helper functions
├── requirements.txt    # Dependencies
└── sample.jpg          # Test file
```

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/haragam22/Code_Script
cd Code_Script/Python/File_Encryption_Decryption
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Usage**

### **1. Encrypt a file**

```bash
python encryptor.py <file_path>
```

**Example:**

```bash
python encryptor.py sample.jpg
```

* Enter a password when prompted.
* Creates an encrypted file: `sample.jpg.enc`.

---

### **2. Decrypt a file**

```bash
python decryptor.py <encrypted_file>
```

**Example:**

```bash
python decryptor.py sample.jpg.enc
```

* Enter the **same password** used for encryption.
* Restores the original file: `sample.jpg`.

---

## **Module Functions (utils.py)**

* `generate_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]`
  Generates a 256-bit AES key from a password using PBKDF2HMAC. Returns `(key, salt)`.

* `encrypt_data(key: bytes, plaintext: bytes) -> bytes`
  Encrypts bytes using AES (CFB mode) and prepends IV.

* `decrypt_data(key: bytes, ciphertext: bytes) -> bytes`
  Decrypts bytes using AES (CFB mode). Expects IV prepended.

