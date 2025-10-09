import asyncio
import os
from datetime import datetime
import argparse
from playwright.async_api import async_playwright

async def take_screenshot(browser, url, output_dir, count):
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(url)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    await page.screenshot(path=filepath, full_page=True)
    print(f"[{count}] Saved screenshot: {filepath}")

    await context.close()

async def main():
    parser = argparse.ArgumentParser(description="Periodic Website Screenshot Tool using Playwright")
    parser.add_argument("url", help="Website URL to take screenshots of")
    parser.add_argument("-i", "--interval", type=int, default=300, help="Interval between screenshots in seconds (default: 300)")
    parser.add_argument("-o", "--output", default="output", help="Directory to save screenshots (default: ./output)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=args.headless)

        count = 1
        try:
            while True:
                await take_screenshot(browser, args.url, args.output, count)
                count += 1
                await asyncio.sleep(args.interval)
        except KeyboardInterrupt:
            print("Stopped by user.")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

