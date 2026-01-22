import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import sys
import os
from datetime import datetime
import re
import json

# Add parent directory to path for imports when running standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ..utils.helpers import clean_text, extract_date, log_site_status, remove_duplicates
except ImportError:
    # Fallback implementations for standalone testing
    def clean_text(text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'<[^>]+>', '', text)
        return text

    def extract_date(date_text):
        # Try to extract date from various formats
        try:
            # Handle format like "10 Desember 2024" or "10 Desember 2024 20:15 WIB"
            if "WIB" in date_text:
                date_part = date_text.replace("WIB", "").strip()
            else:
                date_part = date_text.strip()

            # Convert Indonesian month names
            months = {
                'Januari': '01', 'Februari': '02', 'Maret': '03', 'April': '04',
                'Mei': '05', 'Juni': '06', 'Juli': '07', 'Agustus': '08',
                'September': '09', 'Oktober': '10', 'November': '11', 'Desember': '12'
            }
            for id_month, num_month in months.items():
                if id_month in date_part:
                    date_part = date_part.replace(id_month, num_month)
                    break

            # Try different date formats
            formats = [
                '%d %m %Y %H:%M',
                '%d %m %Y',
                '%d/%m/%Y',
                '%d-%m-%Y'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_part, fmt)
                except:
                    continue
        except:
            pass
        return None

    def log_site_status(site, status, error=None):
        if status == "OK":
            logging.info(f"[{site}] Scraping completed successfully")
        else:
            logging.error(f"[{site}] Scraping failed: {error}")

    def remove_duplicates(articles):
        seen = set()
        unique = []
        for a in articles:
            if a['url'] not in seen:
                seen.add(a['url'])
                unique.append(a)
        return unique

def scrape_antara(keyword="mimika"):
    """
    Scrape news from Antara.com search with keyword
    Returns dict with success status and article data
    """
    articles = []
    search_keywords = [keyword]

    try:
        # Simple headers without compression
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.antaranews.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        # Check if running on Vercel to avoid timeouts
        is_vercel = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None

        if is_vercel:
            logging.info("[Antara News] Vercel detected - limiting scrape to avoid 10s timeout")

        # Get custom limit from env or use defaults
        custom_limit = os.environ.get('SCRAPE_PAGES_LIMIT')
        if custom_limit:
            try:
                actual_max_pages = int(custom_limit)
                logging.info(f"[Antara News] Using custom page limit: {actual_max_pages}")
            except ValueError:
                actual_max_pages = 2 if is_vercel else 5
                logging.warning(f"[Antara News] Invalid SCRAPE_PAGES_LIMIT, using default: {actual_max_pages}")
        else:
             actual_max_pages = 2 if is_vercel else 5

        for keyword in search_keywords:
            logging.info(f"[Antara News] Starting search for keyword: '{keyword}'")

            page = 1
            while True:
                # Check for page limit if on Vercel
                if is_vercel and page > actual_max_pages:
                    logging.info("Vercel page limit reached. Stopping scrape.")
                    break

                search_url = f"https://www.antaranews.com/search?q={keyword}&page={page}"

                try:
                    logging.info(f"[Antara News] Scraping {keyword} page {page}")
                    # Add retry logic for connection issues
                    max_retries = 3
                    for attempt in range(max_retries):
                        try:
                            response = requests.get(search_url, headers=headers, timeout=20)
                            response.raise_for_status()
                            break  # Success, exit retry loop
                        except (requests.exceptions.ConnectionError,
                                requests.exceptions.Timeout,
                                ConnectionError,
                                TimeoutError) as e:
                            if attempt == max_retries - 1:
                                raise  # Re-raise if max retries reached
                            logging.warning(f"[Antara News] Connection error on attempt {attempt + 1}/{max_retries}, retrying...")
                            time.sleep(5 * (attempt + 1))  # Exponential backoff

                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find the main article container
                    article_section = soup.find("div", class_="wrapper__list__article")
                    if not article_section:
                        logging.info(f"[Antara News] No article section found for {keyword} page {page}")
                        break

                    # Find all article cards - Relaxed selector to catch all variations
                    articles_cards = article_section.find_all("div", class_="card__post")

                    if not articles_cards:
                        logging.info(f"[Antara News] No articles found for {keyword} page {page}")
                        break

                    found_on_page = 0
                    for article in articles_cards:
                        try:
                            # Extract from row structure
                            row = article.find("div", class_="row")
                            if not row:
                                continue

                            # Extract from col-md-5 (image column)
                            img_col = row.find("div", class_="col-md-5")
                            if not img_col:
                                continue

                            # Extract link and image
                            link_elem = img_col.find("a")
                            if not link_elem:
                                continue

                            href = link_elem.get('href', '')
                            if not href:
                                continue

                            # Make URL absolute
                            if href.startswith('/'):
                                url = f"https://www.antaranews.com{href}"
                            else:
                                url = href

                            # Extract image URL (User requested: img class="img-fluid lazyloaded")
                            img_url = ""
                            picture_elem = img_col.find("picture")
                            if picture_elem:
                                img_elem = picture_elem.find("img")
                                if img_elem:
                                    img_url = img_elem.get('data-src') or img_elem.get('src', '')
                            
                            # Fallback if picture tag not found, look for direct img with class
                            if not img_url:
                                img_elem = img_col.find("img")
                                if img_elem:
                                    img_url = img_elem.get('data-src') or img_elem.get('src', '')

                            if img_url:
                                logging.info(f"[Antara] Found image: {img_url}")
                            else:
                                logging.warning(f"[Antara] No image found for {url}")

                            # Extract from col-md-7 (content column)
                            detail_col = row.find("div", class_="col-md-7")
                            if not detail_col:
                                continue

                            # Extract title
                            title_elem = detail_col.find("h2", class_="h5")
                            if not title_elem:
                                continue

                            title = clean_text(title_elem.get_text())

                            # Extract date
                            date_str = ""
                            date_elem = detail_col.find("span", class_="text-dark text-capitalize")
                            if date_elem:
                                date_text = clean_text(date_elem.get_text())
                                if date_text:
                                    try:
                                        date_obj = extract_date(date_text)
                                        if date_obj:
                                            date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                                    except:
                                        pass

                            # Extract description
                            description = ""
                            desc_elem = detail_col.find("p")
                            if desc_elem:
                                description = clean_text(desc_elem.get_text())

                            # Extract date from URL pattern if not found in text
                            if not date_str:
                                url_parts = url.split('/')
                                if len(url_parts) >= 5:
                                    article_id = url_parts[-1]
                                    # Extract image URL
                            # User Rule: Picture : img class"img-fluid lazyloaded"
                            img_url = ""
                            # Try Picture tag first
                            picture_elem = img_col.find("picture")
                            if picture_elem:
                                img_elem = picture_elem.find("img")
                                if img_elem:
                                     # Priority: data-src -> src
                                    img_url = img_elem.get('data-src') or img_elem.get('src', '')
                            
                            # Fallback: Direct img tag (if no picture or failed)
                            if not img_url:
                                # Look for img with class 'img-fluid lazyloaded' specifically if possible, or any img
                                img_elem = img_col.find("img", class_="img-fluid")
                                if not img_elem:
                                     img_elem = img_col.find("img")
                                
                                if img_elem:
                                    img_url = img_elem.get('data-src') or img_elem.get('src', '')

                            if img_url:
                                logging.info(f"[Antara] Found image: {img_url}")
                            else:
                                logging.warning(f"[Antara] No image found for {url}")

                            # Category Classification
                            # Use helper to normalize based on Title and URL
                            # Pass 'news' as base category since Antara search doesn't explicitly show category in card
                            # (It might perform regex on URL, but helper does that better now)
                            from ..utils.helpers import normalize_category
                            category = normalize_category("news", title, url)

                            # Add article
                            articles.append({
                                'title': title,
                                'url': url,
                                'description': description,
                                'date': date_str,
                                'category': category,
                                'source': 'Antara News',
                                'image_url': img_url,
                                'search_keyword': keyword
                            })
                            found_on_page += 1

                        except Exception as e:
                            logging.debug(f"Error parsing article: {str(e)}")
                            continue

                    if found_on_page == 0:
                        logging.info(f"[Antara News] No valid articles found for {keyword} page {page}")
                        break

                    logging.info(f"[Antara News] Found {found_on_page} articles for '{keyword}' on page {page}")

                    # Check if we should continue to next page
                    # Look for pagination to see if there's a next page
                    pagination = soup.find("div", class_="pagination")
                    if pagination:
                        # Look for "Next" link or check if current page is the last
                        next_links = pagination.find_all("a", href=True)
                        has_next = any("page=" + str(page + 1) in link.get('href', '') for link in next_links)
                        if not has_next:
                            logging.info(f"[Antara News] No more pages found for '{keyword}' (reached page {page})")
                            break
                    else:
                        # Alternative: look for page navigation links
                        page_links = soup.find_all("a", href=re.compile(rf"page={page + 1}"))
                        if not page_links:
                            # Try to find link to next page
                            current_page_link = soup.find("a", string=str(page), class_="active")
                            if current_page_link:
                                next_sibling = current_page_link.find_next_sibling("a")
                                if not next_sibling:
                                    logging.info(f"[Antara News] No more pages found for '{keyword}' (reached page {page})")
                                    break
                            else:
                                # If no pagination found, assume only one page
                                if page > 1:
                                    logging.info(f"[Antara News] No pagination found, stopping at page {page}")
                                    break

                    # Delay between requests - increased to avoid rate limiting
                    time.sleep(random.uniform(1.5, 3.0) if is_vercel else random.uniform(3, 6))
                    page += 1

                    # Safety break for non-Vercel (limit to reasonable number of pages)
                    if not is_vercel and page > 10:
                        logging.info(f"[Antara News] Page limit reached for keyword '{keyword}' (limited to prevent rate limiting)")
                        break

                except Exception as e:
                    logging.warning(f"[Antara News] Error scraping {keyword} page {page}: {str(e)}")
                    break

            # Small delay between different keywords
            time.sleep(random.uniform(1, 2))

        log_site_status("Antara News", "OK")

    except Exception as e:
        log_site_status("Antara News", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Antara scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

    # Final cleanup and deduplication
    unique_articles = remove_duplicates(articles)
    categories = sorted(list(set(a.get('category', 'news') for a in unique_articles)))

    return {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': ['Antara News'],
                'categories': categories,
                'search_keywords': search_keywords
            },
            'articles': unique_articles
        }
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_antara()
    print(json.dumps(result, indent=2))