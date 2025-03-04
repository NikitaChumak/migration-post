# News Fetcher and WordPress Uploader

This project consists of two Python scripts for fetching news from an external source and automatically posting them to a WordPress site via the REST API.

## 📂 Project Structure

/ ├── fetch_news.py # Fetches news from external API and saves to file_news.json ├── upload_news.py # Reads file_news.json and posts articles to WordPress ├── file_news.json # Temporary storage for fetched news (gitignored if needed) └── README.md # This file 


---

## ⚙️ Requirements

- Python 3.8+
- `requests` library

Install with:
```bash
pip install requests
