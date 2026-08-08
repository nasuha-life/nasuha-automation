import os
import time
import json
import requests
from pathlib import Path

TOKEN = os.environ["META_ACCESS_TOKEN"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]
IG_BUSINESS_ID = os.environ["IG_BUSINESS_ID"]

POSTER_PATH = Path("output/poster.png")
CAPTION_PATH = Path("output/caption.txt")

# IMPORTANT:
# This must be a PUBLIC URL that points to poster.png.
# For now we use the GitHub Pages URL. If GitHub Pages is not enabled,
# replace this with a publicly accessible URL (for example Netlify, Cloudinary, or GitHub raw).
PUBLIC_IMAGE_URL = "https://nasuha-life.github.io/nasuha-automation/poster.png"

DEFAULT_CAPTION = (
    "Allah tidak pernah menutup pintu taubat bagi hamba-Nya. "
    "Sekecil apa pun langkah kita untuk kembali kepada-Nya, "
    "rahmat-Nya selalu lebih luas daripada dosa-dosa kita.\\n\\n"
    "Mulailah perjalanan taubatmu hari ini bersama Nasuha.\\n"
    "https://nasuha.life\\n\\n"
    "#NasuhaLife #Taubat #Muhasabah"
)


def load_caption() -> str:
    if CAPTION_PATH.exists():
        return CAPTION_PATH.read_text(encoding="utf-8").strip()
    return DEFAULT_CAPTION


def request_with_retry(method, url, **kwargs):
    delay = 2
    for attempt in range(3):
        try:
            response = requests.request(method, url, timeout=60, **kwargs)
            if response.status_code in (200, 201):
                return response
            if attempt == 2:
                response.raise_for_status()
        except Exception:
            if attempt == 2:
                raise
        time.sleep(delay)
        delay *= 2
    raise RuntimeError("Unreachable retry state")


def upload_facebook_photo(caption: str):
    if not POSTER_PATH.exists():
        raise FileNotFoundError(f"Poster not found: {POSTER_PATH}")

    url = f"https://graph.facebook.com/v23.0/{FB_PAGE_ID}/photos"

    with open(POSTER_PATH, "rb") as image_file:
        files = {
            "source": ("poster.png", image_file, "image/png")
        }
        data = {
            "caption": caption,
            "access_token": TOKEN
        }

        response = request_with_retry(
            "POST",
            url,
            files=files,
            data=data
        )

    result = response.json()
    print("Facebook photo uploaded successfully")
    print(json.dumps(result, indent=2))
    return result


def create_instagram_container(caption: str):
    url = f"https://graph.facebook.com/v23.0/{IG_BUSINESS_ID}/media"

    response = request_with_retry(
        "POST",
        url,
        data={
            "image_url": PUBLIC_IMAGE_URL,
            "caption": caption,
            "access_token": TOKEN
        }
    )

    result = response.json()
    print("Instagram media container created")
    print(json.dumps(result, indent=2))
    return result["id"]


def publish_instagram(container_id: str):
    url = f"https://graph.facebook.com/v23.0/{IG_BUSINESS_ID}/media_publish"

    response = request_with_retry(
        "POST",
        url,
        data={
            "creation_id": container_id,
            "access_token": TOKEN
        }
    )

    result = response.json()
    print("Instagram post published successfully")
    print(json.dumps(result, indent=2))
    return result


def save_log(data):
    Path("output").mkdir(exist_ok=True)
    with open("output/post_log.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    caption = load_caption()

    log = {
        "facebook": None,
        "instagram": None
    }

    try:
        fb = upload_facebook_photo(caption)
        log["facebook"] = fb

        container_id = create_instagram_container(caption)
        ig = publish_instagram(container_id)
        log["instagram"] = ig

        save_log(log)
        print("All publishing completed successfully.")

    except Exception as e:
        save_log({
            "error": str(e)
        })
        print(f"Publishing failed: {e}")
        raise


if __name__ == "__main__":
    main()
