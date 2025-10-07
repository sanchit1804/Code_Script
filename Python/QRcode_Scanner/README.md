# 🧾 QR Code Scanner

A beginner-friendly Python script that scans and decodes QR codes from an image.

---

## 📋 Features
- Reads QR codes from image files (PNG, JPG, etc.)
- Prints the decoded text or URL to the terminal
- Uses simple, widely available libraries (`opencv-python`, `pyzbar`, `Pillow`)

---

## 🚀 Usage

1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Run the script
python qr_scanner.py sample_images/test_qr.png
If the image contains a valid QR code, you’ll see:
✅ QR Code Detected: Hello Hacktoberfest 2025!


📁 Folder structure
qr_code_scanner/
│
├── qr_scanner.py          # main script
├── README.md              # usage instructions
├── requirements.txt       # dependencies
└── sample_images/         # test images
🧠 Notes
Make sure your image path is correct while testing in CLI.
Works with multiple QR codes in one image.
Tested with Python 3.9+.

🎯 Author
Dhanashree Petare
Contribution for Hacktoberfest 2025 under issue #4 (QR Code Scanner)