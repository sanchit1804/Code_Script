import datetime
import os
import sys

try:
    import pyautogui
    USE_PYAUTOGUI = True
except ImportError:
    import mss
    USE_PYAUTOGUI = False

def take_screenshot(save_dir="Screenshots"):
    # Create the folder if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Generate timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)

    # Capture and save the screenshot
    if USE_PYAUTOGUI:
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
    else:
        with mss.mss() as sct:
            sct.shot(output=filepath)

    print(f" Screenshot saved as: {filepath}")

if __name__ == "__main__":
    take_screenshot()
