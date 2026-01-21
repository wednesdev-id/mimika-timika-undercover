# Scraping Architecture & Landing Page Data Analysis

## 1. Landing Page Data Structure
The Mimika/Timika Landing Pages display news aggregated from various sources. The data displayed is normalized from the backend API.

| UI Field | Backend Data Source | Description |
|----------|---------------------|-------------|
| **Image**| `image_url` | Primary visual. Fallback to placeholder if `null`. |
| **Title** | `title` | News headline (max 2 lines). |
| **Date** | `published_at` | Converted to readable format (e.g., "20 Januari 2026"). |
| **Summary**| `summary` / `description` | Short excerpt or first paragraph. |
| **Source** | `source_name` / `source_url` | Origin of the news (e.g., Detik, Kompas). Used for "Read More" link. |
| **Region** | `region` | "mimika", "timika", or "general". Used for filtering. |

---

## 2. Scraping Source Identification
The backend (`mimika_timika_core`) currently implements **6 active scrapers**. 
*Note: Narasi and Tribun are NOT implemented in the current codebase, replaced by Kumparan and Tempo.*

### 🛠️ Source 1: Detik.com
*   **Target URL**: `https://www.detik.com/search/searchall?query={keyword}`
*   **Container**: `div.list-content` -> `article.list-content__item`
*   **HTML Structure**:
    *   **Title**: `h3.media__title` text
    *   **Link**: `a` href
    *   **Image**: `div.media__image` -> `img` (`data-src` or `src`) OR `span.ratiobox img`
    *   **Date**: `div.media__date span[d-time]` (Unix Timestamp)

### 🛠️ Source 2: Kompas.com
*   **Target URL**: `https://search.kompas.com/search?q={keyword}`
*   **Container**: `div.articleList` -> `div.articleItem`
*   **HTML Structure**:
    *   **Title**: `h2.articleTitle` text
    *   **Link**: `a.article-link` href
    *   **Image**: `div.articleItem-img` -> `img` (`data-src` or `src`)
    *   **Date**: `div.articlePost-date` text

### 🛠️ Source 3: Antara News
*   **Target URL**: `https://www.antaranews.com/search?q={keyword}`
*   **Container**: `div.wrapper__list__article` -> `div.card__post`
*   **HTML Structure**:
    *   **Title**: `h2.h5` text
    *   **Link**: `div.col-md-5 a` href
    *   **Image**: `picture img` OR `img.img-fluid` (`data-src` or `src`)
    *   **Date**: `span.text-dark` text

### 🛠️ Source 4: CNN Indonesia
*   **Target URL**: `https://www.cnnindonesia.com/search/?query={keyword}`
*   **Strategy**: Simplified Link Traversal
*   **HTML Structure**:
    *   Finds all `a` tags.
    *   **Filter**: `href` must contain `cnnindonesia.com` AND `/berita/`.
    *   **Title**: `h1`, `h2`, `h3` inside the link.
    *   **Image**: Not explicitly targeted in search view (often missing in simplified scraper).

### 🛠️ Source 5: Kumparan
*   **Target URL**: `https://kumparan.com/search/{keyword}`
*   **Strategy**: Simplified Link Traversal
*   **HTML Structure**:
    *   Finds all `a` tags.
    *   **Filter**: `href` must contain `kumparan.com` AND length > 10.
    *   **Title**: `h1`...`h4` inside the link.
    *   **Image**: Not explicitly targeted.

### 🛠️ Source 6: Tempo.co
*   **Target URL**: `https://www.tempo.co/search?q={keyword}`
*   **Strategy**: Simplified Link Traversal
*   **HTML Structure**:
    *   Finds all `a` tags.
    *   **Filter**: `href` must contain `tempo.co` AND (`/berita/` OR `/read/`).
    *   **Title**: `h1`...`h4` inside the link.
    *   **Desc**: `div` with class matching `desc|summary|excerpt`.

### 🛠️ Source 7: SeputarPapua.com
*   **Target URL**: `https://seputarpapua.com/?s={keyword}&post_type=post`
*   **Container**: `div.widget-content` -> `div.article-item`
*   **HTML Structure**:
    *   **Title**: `div.article-text` -> `h3` -> `a` text
    *   **Link**: `div.article-text` -> `h3` -> `a` href
    *   **Image**: `div.article-image` -> `img` src
    *   **Desc**: `div.article-text` -> `div.snippet` text
    *   **Date**: Extracted from Detail Page (meta tags or date classes).

---

## 3. Data Collection Summary
The scrapers collect the following unified data model for each article:

```json
{
  "title": "String (Cleaned)",
  "url": "String (Absolute URL)",
  "description": "String (Excerpt)",
  "date": "String (YYYY-MM-DD HH:MM:SS)",
  "category": "String (Normalized: 'news', 'nasional', etc.)",
  "source": "String (e.g., 'Detik.com')",
  "image_url": "String (URL to image)",
  "search_keyword": "String (The keyword used to find this, e.g., 'mimika')"
}
```

## 4. Vercel Optimization Strategy (Serverless Constraints)
To ensure reliable scraping within Vercel's **10-second Function Timeout** (Free Tier):

1.  **Small Batches**: Scrapers are limited to **5-10 articles** per execution.
    *   *Reason*: Visiting Detail Pages (e.g., SeputarPapua) takes ~1.5s per article. Procssing 20 articles would take ~30s, causing a timeout.
2.  **High Frequency**: The Scheduler runs **Every 30 Minutes** (instead of hourly).
    *   *Result*: 1 Day = 48 runs x 10 articles = **480 potential articles/day**.
    *   This accumulates data over time without crashing the server.
3.  **Timeout Protection**: Individual scrapers have internal request timeouts (10-15s) to fail fast rather than hang the entire engine.
