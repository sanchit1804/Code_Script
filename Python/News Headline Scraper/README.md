# News Headline Scraper (Python)

A simple Python script that fetches news headlines from various news outlets using their public RSS feeds and saves them to a JSOn file, no API keys are required in the process.
---

## 🚀 Features
- Saves headlines to JSON with timestamps.
- Multiple trusted sources: BBC, Reuters, CNN, NYTimes, HackerNews
- No API key needed (uses official RSS feeds)

---
## Usage

python3 news_headline_scraper.py

Output: 
Fetching: BBC
Fetching: Reuters
Fetching: CNN
Fetching: NYTimes
Fetching: HackerNews
Headlines saved to the file

## 🧰 Requirements

Install the dependencies using pip:
```bash
pip install feedparser