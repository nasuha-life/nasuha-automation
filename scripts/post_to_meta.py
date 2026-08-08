import os
import json
import requests
from pathlib import Path

TOKEN = os.environ["META_ACCESS_TOKEN"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]

POSTER = Path("output/poster.png")
CAPTION = Path("output/caption.txt")

if not POSTER.exists():
    raise FileNotFoundError("output/poster.png not found")

caption = CAPTION.read_text(encoding="utf-8") if CAPTION.exists() else "https://nasuha.life"

url = f"https://graph.facebook.com/v23.0/{FB_PAGE_ID}/photos"

with open(POSTER, "rb") as f:
    response = requests.post(
        url,
        files={"source": f},
        data={
            "caption": caption,
            "access_token": TOKEN,
        },
        timeout=60,
    )

print(response.status_code)
print(response.text)

response.raise_for_status()

print("Facebook post published successfully.")
