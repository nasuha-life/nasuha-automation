import os
import requests
from caption_generator import generate_caption

TOKEN = os.environ["META_ACCESS_TOKEN"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]
IG_BUSINESS_ID = os.environ["IG_BUSINESS_ID"]

def check_page():
    url = f"https://graph.facebook.com/v25.0/{FB_PAGE_ID}?fields=id,name&access_token={TOKEN}"
    r = requests.get(url, timeout=30)
    print("Facebook:", r.status_code, r.text)

def check_instagram():
    url = f"https://graph.facebook.com/v25.0/{IG_BUSINESS_ID}?fields=id,username&access_token={TOKEN}"
    r = requests.get(url, timeout=30)
    print("Instagram:", r.status_code, r.text)

if __name__ == "__main__":
    print(generate_caption())
    check_page()
    check_instagram()
