import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# Настройки WordPress
WP_SITE = ""
WP_USER = ""
WP_PASSWORD = ""
CATEGORY_ID = 1
FEATURED_IMAGE_ID = 1661  # placeholder3-2.png

HEADERS = {
    "User-Agent": "MyPythonScript/1.0"
}

def convert_date_to_iso(date_str):
    return f"{date_str}T00:00:00"

def get_post_content(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Ошибка загрузки страницы {url}")
        return None, None, None

    soup = BeautifulSoup(response.text, "html.parser")

    title_element = soup.select_one(".single_news_wrap .head .content_wrap .title")
    if not title_element:
        print(f"❌ Заголовок не найден на странице {url}")
        return None, None, None

    title = title_element.get_text(strip=True)

    date_element = soup.select_one(".single_news_wrap .head .content_wrap .date")
    if not date_element:
        print(f"❌ Дата не найдена на странице {url}")
        return None, None, None

    raw_date = date_element.get_text(strip=True)
    date_obj = datetime.strptime(raw_date, "%b %d %Y")
    post_date = date_obj.strftime("%Y-%m-%d")

    content_div = soup.select_one(".single_news_wrap .content .left")
    if not content_div:
        print(f"❌ Контент не найден на странице {url}")
        return None, None, None

    content_html = str(content_div)

    return title, post_date, content_html

def get_or_create_tags(tags, auth):
    tag_ids = []
    for tag in tags:
        search_url = f"{WP_SITE}/wp-json/wp/v2/tags"
        response = requests.get(search_url, params={"search": tag}, headers=HEADERS, auth=auth)

        if response.status_code == 200 and response.json():
            tag_ids.append(response.json()[0]["id"])
        else:
            create_response = requests.post(search_url, json={"name": tag}, headers=HEADERS, auth=auth)
            if create_response.status_code == 201:
                tag_ids.append(create_response.json()["id"])
            else:
                print(f"⚠️ Ошибка при создании тега '{tag}': {create_response.text}")
    return tag_ids

def create_wordpress_post(article, auth):
    title, post_date, content_html = get_post_content(article['link'])
    if not title or not content_html:
        print(f"❌ Пропускаем {article['link']} — контент не найден")
        return

    tags = get_or_create_tags(article.get('tags') or [], auth)  # Защита от None

    post_data = {
        "title": title,
        "status": "publish",
        "date": convert_date_to_iso(post_date),
        "content": content_html,
        "categories": [CATEGORY_ID],
        "tags": tags
    }

    response = requests.post(f"{WP_SITE}/wp-json/wp/v2/posts", json=post_data, headers=HEADERS, auth=auth)

    if response.status_code == 201:
        post_id = response.json()["id"]
        print(f"✅ Пост создан: {title}")
        set_featured_image(post_id, auth)
    else:
        print(f"❌ Ошибка при создании поста: {response.text}")

def set_featured_image(post_id, auth):
    url = f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}"
    data = {"featured_media": FEATURED_IMAGE_ID}

    response = requests.post(url, json=data, headers=HEADERS, auth=auth)
    if response.status_code == 200:
        print(f"✅ Изображение placeholder3-2 установлено для поста {post_id}")
    else:
        print(f"❌ Ошибка при установке изображения: {response.text}")

def load_news():
    with open('file_news.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    all_news = load_news()
    auth = (WP_USER, WP_PASSWORD)

    for article in all_news:
        if "file.com/single-news" in article["link"]:
            create_wordpress_post(article, auth)

if __name__ == "__main__":
    main()
