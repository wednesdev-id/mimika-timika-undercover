import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd


# """Situs Detik.com"""
# def pagination_test():
#     urls = []
#     # Test with only 2 pages for faster execution
#     for i in range(1, 101):
#         url = f"https://www.detik.com/search/searchall?query=mimika%20timika&page={i}&result_type=latest"
#         urls.append(url)
#     return urls

# def get_html_test():
#     urls = pagination_test()
#     html = []
#     for url in urls:
#         print(f"Fetching: {url}")
#         r = requests.get(url)
#         time.sleep(5)
#         html.append(r.text)
#     return html

# def parsing_test():
#     html = get_html_test()
#     berita = []

#     for i in html:
#         soup = BeautifulSoup(i, 'html.parser')
#         main = soup.find('div', class_="container-fluid")
#         articles = main.find('div', class_= "column-6")
#         article = articles.find_all('div', class_="list-content")

#         for links in article:
#             links = links.find_all('article', class_="list-content__item")
#             for link in links:
#                 title = link.find('h3', class_="media__title").text.strip()
#                 href = link.find('a')['href']
#                 desc = link.find('div', class_="media__desc")
#                 if desc:
#                     desc = desc.text.strip()
#                 else:
#                     desc = " - "
#                 time_timestamp = link.find('div', class_="media__date").find('span')['d-time']
#                 # Store as datetime object for proper sorting
#                 time_datetime = datetime.fromtimestamp(int(time_timestamp), tz=ZoneInfo("Asia/Jakarta"))
#                 # Convert to string format for display
#                 time_str = time_datetime.strftime("%d/%m/%y")

#                 data = {
#                     "title": title,
#                     "link": href,
#                     "desc": desc,
#                     "time": time_str,
#                     "datetime_obj": time_datetime  # Add datetime object for sorting
#                 }
#                 berita.append(data)

#     # Sort all articles by datetime (newest first) - moved outside the loop
#     berita.sort(key=lambda x: x["datetime_obj"], reverse=True)

#     # Remove datetime_obj from final data
#     for item in berita:
#         del item["datetime_obj"]

#     return berita

# def convert_test():
#     berita = parsing_test()
#     print(f"Total berita yang berhasil di-scrape: {len(berita)}")

#     # Show first 5 articles to verify sorting
#     print("\n5 berita terbaru (terurut dari yang terbaru):")
#     for i, item in enumerate(berita[:5]):
#         print(f"{i+1}. {item['time']} - {item['title'][:50]}...")

#     df = pd.DataFrame(berita)
#     df.to_excel("test_sorted.xlsx", index=False)
#     print(f"\nBerhasil disimpan ke test_sorted.xlsx")

# if __name__ == "__main__":
#     convert_test()


# """Situs Antara News"""
# def pagination_test():
#     urls = []
#     for i in range(1, 6):  # Test with only 5 pages for faster execution
#         url = f"https://www.antaranews.com/search?q=mimika+timika&page={i}"
#         urls.append(url)
#     return urls

# def get_html_test():
#     urls = pagination_test()
#     html = []
#     for url in urls:
#         print(f"Fetching: {url}")
#         r = requests.get(url)
#         print(f"Status code for {url}: {r.status_code}")  # Add this line to print the status coder.status_code)
#         time.sleep(5)
#         html.append(r.text)
#     return html

# def parsing_test():
#     html = get_html_test()
#     berita = []

#     for i in html:
#         soup = BeautifulSoup(i, 'html.parser')
#         main_section = soup.find('section')
           
# if __name__ == "__main__":
#     parsing_test()

"""Situs tribunnews.com"""
def pagination_test():
    urls = []
    for i in range(1, 6):  # Test with only 5 pages for faster execution
        url = f"https://www.tribunnews.com/search?q=mimika+timika&cx=partner-pub-f6e618dd8369c4970&cof=FORID%3A10&ie=UTF-8&siteurl=tribunnews.com#gsc.tab=0&gsc.q=mimika%20timika&gsc.page={i}"
        urls.append(url)
        print(urls)
    return urls

def get_html_test():
    urls = pagination_test()
    html = []
    for url in urls:
        print(f"Fetching: {url}")
        r = requests.get(url)
        print(f"Status code for {url}: {r.status_code}")  # Add this line to print the status coder.status_code)
        # time.sleep(5)
        # html.append(r.text)
    return html

if __name__ == "__main__":
    get_html_test()