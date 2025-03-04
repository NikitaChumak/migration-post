import requests
import json
import os

# Constants and configuration
CATEGORY_ID = 1  # Default WordPress category ID (adjust if needed)

HEADERS = {
    "User-Agent": "MyPythonScript/1.0"
}


def convert_date_to_iso(date_str):
    """
    Converts date string from YYYY-MM-DD to ISO 8601 (used by WordPress API).
    """
    return f"{date_str}T00:00:00"


def upload_featured_image(post_id, image_url, auth, wp_site):
    """
    Downloads the image from the given URL and uploads it to the WordPress media library.
    Attaches the uploaded image as the featured image for the post.
    """
    image_data = requests.get(image_url).content
    filename = os.path.basename(image_url)

    media_url = f"{wp_site}/wp-json/wp/v2/media"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "User-Agent": "MyPythonScript/1.0"
    }
    files = {"file": (filename, image_data)}

    response = requests.post(media_url, files=files, headers=headers, auth=auth)
    if response.status_code == 201:
        media_id = response.json()["id"]
        update_post_with_image(post_id, media_id, auth, wp_site)
    else:
        print(f"❌ Failed to upload image: {response.text}")


def update_post_with_image(post_id, media_id, auth, wp_site):
    """
    Sets the uploaded media file as the featured image for the given post.
    """
    url = f"{wp_site}/wp-json/wp/v2/posts/{post_id}"
    data = {"featured_media": media_id}
    response = requests.post(url, json=data, headers=HEADERS, auth=auth)
    if response.status_code != 200:
        print(f"❌ Failed to set featured image: {response.text}")


def get_or_create_tags(tags, auth, wp_site):
    """
    Fetches existing tags from WordPress or creates new ones if needed.
    Returns a list of tag IDs.
    """
    tag_ids = []
    for tag in tags:
        search_url = f"{wp_site}/wp-json/wp/v2/tags"
        response = requests.get(search_url, params={"search": tag}, headers=HEADERS, auth=auth)

        if response.status_code == 200 and response.json():
            tag_ids.append(response.json()[0]["id"])
        else:
            create_response = requests.post(search_url, json={"name": tag}, headers=HEADERS, auth=auth)
            if create_response.status_code == 201:
                tag_ids.append(create_response.json()["id"])
            else:
                print(f"⚠️ Failed to create tag '{tag}': {create_response.text}")
    return tag_ids


def update_acf_fields(post_id, external_link, hide_date_display, auth, wp_site):
    """
    Updates custom ACF fields for a given post.
    """
    url = f"{wp_site}/wp-json/acf/v3/posts/{post_id}"

    data = {
        "fields": {
            "external_link": external_link,
            "hide_date_display": 1 if hide_date_display else 0
        }
    }

    response = requests.post(url, json=data, headers=HEADERS, auth=auth)

    if response.status_code == 200:
        print(f"✅ ACF fields updated for post {post_id}")
    else:
        print(f"❌ Failed to update ACF fields: {response.text}")


def create_wordpress_post(article, auth, wp_site):
    """
    Creates a new WordPress post and handles all related operations:
    - Creating post
    - Uploading featured image
    - Setting ACF fields
    """
    tags = get_or_create_tags(article['tags'], auth, wp_site)

    wp_date = convert_date_to_iso(article['date'])

    post_data = {
        "title": article['title'],
        "status": "publish",
        "date": wp_date,
        "content": f'<p><a href="{article["link"]}" target="_blank">Read Original</a></p>',
        "categories": [CATEGORY_ID],
        "tags": tags
    }

    response = requests.post(f"{wp_site}/wp-json/wp/v2/posts", json=post_data, headers=HEADERS, auth=auth)

    if response.status_code == 201:
        post_id = response.json()["id"]
        print(f"✅ Post created: {article['title']}")

        # Upload and attach featured image
        upload_featured_image(post_id, article["image"], auth, wp_site)

        # Update ACF fields
        update_acf_fields(post_id, article["link"], True, auth, wp_site)  # Set hide_date_display to True
    else:
        print(f"❌ Failed to create post: {response.text}")


def load_news(filename='file_news.json'):
    """
    Loads previously fetched news articles from JSON file.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """
    Main function: reads articles from file and uploads them to WordPress.
    """
    # Fetch credentials from environment variables (recommended for security)
    wp_site = os.getenv('WP_SITE')
    wp_user = os.getenv('WP_USER')
    wp_password = os.getenv('WP_PASSWORD')

    if not all([wp_site, wp_user, wp_password]):
        print("❌ Missing WordPress credentials. Set WP_SITE, WP_USER, WP_PASSWORD environment variables.")
        return

    articles = load_news()

    auth = (wp_user, wp_password)

    for article in articles:
        if "mtch.com/single-news" not in article["link"]:  # Example filter (optional)
            create_wordpress_post(article, auth, wp_site)


if __name__ == "__main__":
    main()
