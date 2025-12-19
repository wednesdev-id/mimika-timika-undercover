import requests
import re

cx = "4593c3f3750fa44b5"
url = f"https://cse.google.com/cse.js?cx={cx}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
content = response.text

# Search for cse_token in cse.js
token_match = re.search(r'"cse_token":\s*"([^"]+)"', content)
if token_match:
    print(f"Found token in cse.js: {token_match.group(1)}")
else:
    print("Token not found in cse.js")

# Sometimes it's in a different format
token_match = re.search(r'cse_token\s*:\s*"([^"]+)"', content)
if token_match:
    print(f"Found token (alt format): {token_match.group(1)}")

# Example result URL
# https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=en&source=gcsc&gss=.com&start=0&cx=4593c3f3750fa44b5&q=mimika&safe=active&cse_tok=...
