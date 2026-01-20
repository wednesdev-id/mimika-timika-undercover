
import requests
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

try:
    url = "https://www.antaranews.com/search?q=mimika"
    print(f"Fetching {url}...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
