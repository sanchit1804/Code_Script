"""
QR Code Scanner 🧾
-------------------
A simple Python script to read and decode QR codes from an image file.

Dependencies:
    pip install opencv-python pyzbar Pillow

Usage:
    python qr_scanner.py <path_to_image>

Example:
    python qr_scanner.py sample_images/test_qr.png
"""

import sys
import cv2
from pyzbar.pyzbar import decode
from PIL import Image


def scan_qr_code(image_path):
    """
    Reads an image and decodes QR codes inside it.
    Returns a list of decoded strings (text/URLs).
    """
    try:
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        if img is None:
            print("⚠️ Could not read the image. Check the path.")
            return []

        # Decode any QR codes present in the image
        qr_codes = decode(img)
        if not qr_codes:
            print("❌ No QR code found in the image.")
            return []

        decoded_texts = []
        for qr in qr_codes:
            data = qr.data.decode('utf-8')
            decoded_texts.append(data)
            print(f"✅ QR Code Detected: {data}")

        return decoded_texts

    except Exception as e:
        print(f"🚫 Error: {e}")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qr_scanner.py <path_to_image>")
    else:
        image_path = sys.argv[1]
        scan_qr_code(image_path)
