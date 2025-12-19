import requests
import re
import json

cx = "4593c3f3750fa44b5"
keyword = "mimika"

def get_cse_token(cx):
    url = f"https://cse.google.com/cse.js?cx={cx}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.tribunnews.com/"
    }
    response = requests.get(url, headers=headers, timeout=10)
    match = re.search(r'"cse_token":\s*"([^"]+)"', response.text)
    if match:
        return match.group(1)
    return None

token = get_cse_token(cx)
print(f"Token: {token}")

if token:
    search_url = f"https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=id&source=gcsc&gss=.com&start=0&cx={cx}&q={keyword}&safe=active&cse_tok={token}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.tribunnews.com/"
    }
    response = requests.get(search_url, headers=headers, timeout=15)
    print(f"Status Code: {response.status_code}")
    print(f"Response Content (first 500 chars): {response.text[:500]}")
    
    try:
        json_data = response.json()
        print("Successfully parsed as JSON")
    except:
        # Try stripping comments
        try:
            cleaned = re.sub(r'/\*.*?\*/', '', response.text, flags=re.DOTALL).strip()
            json_data = json.loads(cleaned)
            print("Successfully parsed as JSON after stripping comments")
        except Exception as e:
            print(f"Failed to parse: {e}")
