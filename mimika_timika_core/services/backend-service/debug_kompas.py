import requests
from bs4 import BeautifulSoup

def test_scrape():
    url = "https://search.kompas.com/search?q=mimika+timika&page=1&sort=latest&site_id=all"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='articleItem')
        print(f"Found {len(items)} items")
        
        for i, item in enumerate(items[:3]):
            print(f"\nItem {i+1}:")
            title = item.find('h2').get_text(strip=True) if item.find('h2') else "No Title"
            print(f"Title: {title}")
            
            # Test different selectors
            # 1. User requested
            wrap = item.find('div', class_='articleItem-wrap')
            img_src = "Not Found"
            if wrap:
                img_div = wrap.find('div', class_='articleItem-img')
                if img_div:
                    img = img_div.find('img')
                    if img:
                        img_src = img.get('src')
                        print(f"Found via wrap/img-div: {img_src}")
                        print(f"Data-src via wrap: {img.get('data-src')}")
            
            # 2. Direct img
            direct_img = item.find('img')
            if direct_img:
                print(f"Direct img src: {direct_img.get('src')}")
                print(f"Direct img data-src: {direct_img.get('data-src')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_scrape()
