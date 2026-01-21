# Client-Side to Server-Side Filtering Migration Plan

## Problem
The current category filtering is client-side only. This is inefficient for large datasets. The user wants to implement server-side filtering for 8 specific categories.

## Discrepancies
Frontend Categories differ slightly from Backbone Normalized Categories.
- **Politik** -> Backend: **Pemerintahan**
- **Sosial** -> Backend: **Sosial & Budaya**
- **Budaya** -> Backend: **Sosial & Budaya**

## Proposed Changes

### Core Backend (`mimika_timika_core`)
#### [MODIFY] [main.py](file:///d:/MY%20WORK/Wednes.Dev/Papua%20News/mimika_timika_core/services/backend-service/app/main.py)
- Update `get_articles` endpoint to accept `category: Optional[str]`.
- Implement mapping logic:
    ```python
    if category:
        if category == "Politik":
            target_cats = ["Pemerintahan"]
        elif category in ["Sosial", "Budaya"]:
            target_cats = ["Sosial & Budaya"]
        else:
            target_cats = [category]
        query = query.filter(models.Article.category.in_(target_cats))
    ```
- This ensures that when a user filters by "Politik", we get "Pemerintahan" articles.

### Frontend (`mimika_landing_page` & `timika_landing_page`)
#### [MODIFY] [api.ts](file:///d:/MY%20WORK/Wednes.Dev/Papua%20News/mimika_landing_page/src/services/api.ts) (and Timika version)
- Ensure `category` param is correctly appended to the URL. (Already exists, just verify/ensure enabled).

#### [MODIFY] [Index.tsx](file:///d:/MY%20WORK/Wednes.Dev/Papua%20News/mimika_landing_page/src/pages/Index.tsx) (and Timika version)
- Update `useEffect` to trigger `fetchNews` whenever `selectedCategory` changes.
- Remove client-side `filteredNews` logic.
- Use `news` state directly.

## Verification Plan

### Manual Verification
1.  **Start Backend**: Ensure `backend-service` is running.
2.  **Start Frontend**: Ensure `mimika_landing_page` is running.
3.  **Navigate to Home**: Open `http://localhost:8080` (or relevant port).
4.  **Click Categories**:
    - Click "Politik" -> Verify Network Request to `/articles?region=mimika&category=Politik`.
    - Verify Response contains items with `category: "Pemerintahan"`.
    - Click "Sosial" -> Verify items with `category: "Sosial & Budaya"`.
5.  **Check Empty State**: Click a category with no news (likely "Lingkungan"), verify "Tidak ada berita" message appears.
