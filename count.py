import json

def count_external_posts(file_path):
    
    with open(file_path, 'r', encoding='utf-8') as f:
        all_news = json.load(f)

    external_posts = [news for news in all_news if "" not in news["link"]]
    
    print(f"✅ Количество внешних постов: {len(external_posts)}")

if __name__ == "__main__":
    count_external_posts('')  
