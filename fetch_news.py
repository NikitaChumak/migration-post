import json
import requests
from datetime import datetime

# Example source URL (replace with your actual source)
NEWS_API_URL = "https://example.com/api/news"  # Replace with real URL
HEADERS = {
    "User-Agent": "MyPythonScript/1.0"
}

def fetch_news():
    """
    Fetches news articles from external API and saves them into file_news.json file.
    Adjust the parsing logic based on the actual structure of the response.
    """
    response = requests.get(NEWS_API_URL, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Failed to fetch news: {response.status_code}")
        return []

    data = response.json()

    articles = []
    for item in data.get("articles", []):
        articles.append({
            "title": item["title"],
            "link": item["url"],
            "image": item["image_url"],
            "date": item["published_date"],
            "tags": item.get("tags", ["News"])  # Fallback to 'News' tag if tags missing
        })

    return articles

def save_news_to_file(articles, filename='file_news.json'):
    """
    Saves fetched articles to a JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"✅ {len(articles)} articles saved to {filename}")

def main():
    """
    Main function to fetch and save articles.
    """
    articles = fetch_news()
    if articles:
        save_news_to_file(articles)
    else:
        print("❌ No articles fetched.")

if __name__ == "__main__":
    main()
