import requests

WP_SITE = ""
WP_USER = ""
WP_PASSWORD = ""  # сюда вставь Application Password

def test_api_access():
    url = f"{WP_SITE}/wp-json/wp/v2/posts"
    
    # Важно: просто (username, password), без HTTPBasicAuth
    auth = (WP_USER, WP_PASSWORD)

    headers = {
        "User-Agent": "MyPythonScript/1.0"
    }

    response = requests.get(url, auth=auth, headers=headers)

    print(f"Статус: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    test_api_access()
