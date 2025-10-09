````markdown
# 📸 Screenshot Automation Bot

`screenshot_automation_bot.py` is a Python CLI tool that **automates taking periodic full-page screenshots** of any website using [Playwright](https://playwright.dev/).

Ideal for monitoring visual changes, archiving web content, or debugging dynamic pages over time.

---

## 🚀 How to Run

After installing the required dependencies (see below), run the script as follows:

```bash
python screenshot_automation_bot.py <url> [options]
````

### ⚙️ Command-Line Options

| Option | Description | Default |
| :--- | :--- | :--- |
| `<url>` | (Required) The target website URL to screenshot | `None` |
| `-i`, `--interval` | Interval (in seconds) between each screenshot | `300` (5 minutes) |
| `-o`, `--output` | Output directory to save screenshots | `output/` |
| `--headless` | Run the browser in headless mode (no GUI) | `False` (GUI is shown by default) |

### 📂 Example Usage

1.  **Basic example (every 5 minutes):**

    ```bash
    python screenshot_automation_bot.py [https://example.com](https://example.com)
    ```

2.  **Custom interval and output directory:**

    ```bash
    python screenshot_automation_bot.py [https://example.com](https://example.com) -i 600 -o snapshots
    ```

3.  **Run in headless mode:**

    ```bash
    python screenshot_automation_bot.py [https://example.com](https://example.com) --headless
    ```

## 🖼 Output

Screenshots are saved in the specified output folder using a timestamped filename format:

```
output/
├── screenshot_20251009_141500.png
├── screenshot_20251009_142000.png
...
```

## 🛠 Requirements

  * Python 3.7 or later
  * Playwright (Python)

### Install Requirements

```bash
pip install -r requirements.txt
playwright install
```

## 🧯 Stop the Script

Use `Ctrl + C` to safely stop the script when running in a terminal.

```
```
