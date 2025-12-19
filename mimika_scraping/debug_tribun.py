import requests
import re

url = "https://www.tribunnews.com/search?q=mimika"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
html = response.text

# Try to find cse_tok
token_match = re.search(r'"cse_token":\s*"([^"]+)"', html)
if token_match:
    print(f"Found token via cse_token: {token_match.group(1)}")
else:
    # Try another common pattern
    token_match = re.search(r'cse_tok=(.+?)[&"]', html)
    if token_match:
        print(f"Found token via cse_tok=: {token_match.group(1)}")
    else:
        # Search for any string that looks like a token
        token_match = re.search(r'"token":\s*"([^"]+)"', html)
        if token_match:
            print(f"Found token via token: {token_match.group(1)}")
        else:
            # Maybe it's in window.__gcse
            token_match = re.search(r'"scb":\s*"([^"]+)"', html)
            if token_match:
                print(f"Found something in scb: {token_match.group(1)}")
            else:
                print("Token not found in raw HTML")

# Also check for CX
cx_match = re.search(r'cx=([0-9a-z:]+)', html)
if cx_match:
    print(f"Found CX via cx=: {cx_match.group(1)}")
else:
    cx_match = re.search(r'"cx":\s*"([^"]+)"', html)
    if cx_match:
        print(f"Found CX via 'cx': {cx_match.group(1)}")
