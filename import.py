import requests
import json
import os
from requests.auth import HTTPBasicAuth

# Настройки
WP_SITE = ""  # замени на свой сайт
WP_USER = ""        # логин
WP_PASSWORD = ""  # пароль приложения (не обычный пароль!)

CATEGORY_ID = 1  # ID категории, куда добавлять посты

# Функция создания или получения тега
def get_or_create_tags(tags, auth):
    tag_ids = []
    for tag in tags:
        response = requests.get(f"{WP_SITE}/wp-json/wp/v2/tags", params={"search": tag}, auth=auth)
        if response.status_code == 200 and response.json():
            tag_ids.append(response.json()[0]["id"])
        else:
            create_response = requests.post(f"{WP_SITE}/wp-json/wp/v2/tags", json={"name": tag}, auth=auth)
            if create_response.status_code == 201:
                tag_ids.append(create_response.json()["id"])
    return tag_ids

# Функция загрузки изображения и привязки его к посту
def upload_featured_image(post_id, image_url, auth):
    image_data = requests.get(image_url).content
    filename = os.path.basename(image_url)

    media_url = f"{WP_SITE}/wp-json/wp/v2/media"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    files = {"file": (filename, image_data)}

    response = requests.post(media_url, files=files, headers=headers, auth=auth)
    if response.status_code == 201:
        media_id = response.json()["id"]
        update_post_with_image(post_id, media_id, auth)
    else:
        print(f"❌ Ошибка при загрузке изображения: {response.text}")

def update_post_with_image(post_id, media_id, auth):
    url = f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}"
    data = {"featured_media": media_id}
    requests.post(url, json=data, auth=auth)

# Функция создания поста
def create_wordpress_post(article, auth):
    tags = get_or_create_tags(article['tags'], auth)

    post_data = {
        "title": article['title'],
        "status": "publish",
        "date": article['date'],
        "content": f'<p><a href="{article["link"]}" target="_blank">Читать оригинал</a></p>',
        "categories": [CATEGORY_ID],  # добавляем в категорию ID 1
        "tags": tags,
        "acf": {
            "external_link": article["link"]
        }
    }

    response = requests.post(f"{WP_SITE}/wp-json/wp/v2/posts", json=post_data, auth=auth)

    if response.status_code == 201:
        post_id = response.json()["id"]
        print(f"✅ Пост создан: {article['title']}")

        # Загружаем картинку
        upload_featured_image(post_id, article["image"], auth)
    else:
        print(f"❌ Ошибка при создании поста: {response.text}")

# Загрузка данных из твоего JSON-файла
with open('', 'r', encoding='utf-8') as f:
    all_news = json.load(f)

# Обработка только внешних ссылок
auth = HTTPBasicAuth(WP_USER, WP_PASSWORD)

for news in all_news:
    if "" not in news["link"]:
        create_wordpress_post(news, auth)
