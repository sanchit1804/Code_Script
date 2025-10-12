# 📸 Screenshot Capture Tool

A simple Python tool that captures your **screen** and automatically saves it with a **timestamped filename**.  
This project is perfect for logging visual data, monitoring screen changes, or quickly taking snapshots.

---

## 📜 What the Script Does

- Captures a **full-screen screenshot** of your current display.  
- Automatically generates a **timestamped filename** (e.g., `screenshot_2025-10-11_22-05-30.png`).  
- Saves the screenshot in a folder called **Screenshots**, which is **automatically created** if it doesn’t exist.  
- Auto-detects Python version and uses the best compatible library (`pyautogui` for ≤3.12, `mss` for 3.13+).  
- Prints a success message showing where the file was saved.

---

## 🛠️ How to Run the Script

### **Prerequisites**
Make sure you have **Python 3** installed.  
Install the required libraries:

```bash
pip install pyautogui mss
```