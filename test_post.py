import requests

# Настройки WordPress
WP_SITE = ""
WP_USER = ""
WP_PASSWORD = ""
POST_ID = 1668  
FEATURED_IMAGE_ID = 1683  

HEADERS = {
    "User-Agent": "MyPythonScript/1.0",
    "Content-Type": "application/json"
}

def set_featured_image(post_id, auth):
    """ Обновляет featured image для поста через PUT """
    url = f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}"

    data = {
        "featured_media": FEATURED_IMAGE_ID
    }

    response = requests.put(url, json=data, headers=HEADERS, auth=auth)

    if response.status_code == 200:
        print(f"✅ Изображение успешно установлено для поста {post_id}")
        print(response.json())
    else:
        print(f"❌ Ошибка при установке изображения: {response.status_code}")
        print(response.text)

def main():
    auth = (WP_USER, WP_PASSWORD)
    set_featured_image(POST_ID, auth)

if __name__ == "__main__":
    main()
