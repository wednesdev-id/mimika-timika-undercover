import { siteConfig } from "../config/site";
import { NewsArticle } from "@/shared/types"; // Shared Type

const API_BASE_URL = "https://papuanews-engine.vercel.app"; // Direct connection to Vercel Backend

// Re-export type if needed locally, or use directly from component
export type { NewsArticle };

// Interface matching backend response structure
interface BackendArticle {
    id: number;
    title: string;
    summary: string;
    image_url: string | null;
    category: string;
    region: string;
    published_at: string;
    source_url: string;
}

export interface Pagination {
    current_page: number;
    total_pages: number;
    total_items: number;
    page_size: number;
}

export interface NewsResponse {
    data: NewsArticle[];
    pagination: Pagination;
}

// Reverted to original simple fetch
export const fetchNews = async (region?: string, category?: string): Promise<NewsArticle[]> => {
    const targetRegion = region || siteConfig.region;
    const params = new URLSearchParams();
    params.append("region", targetRegion);
    if (category && category !== "Semua") params.append("category", category);

    try {
        const response = await fetch(`${API_BASE_URL}/articles?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch news");

        const json = await response.json();

        return json.map((item: BackendArticle) => ({
            id: item.id,
            title: item.title,
            summary: item.summary,
            image: item.image_url || "/placeholder.svg",
            category: item.category,
            region: item.region,
            published_at: item.published_at,
            date: formatDate(item.published_at),
            url: item.source_url
        }));
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
};

export const fetchNewsById = async (id: number | string): Promise<NewsArticle | null> => {
    try {
        const response = await fetch(`${API_BASE_URL}/articles/${id}`);
        if (!response.ok) throw new Error("Failed to fetch news detail");

        const item: BackendArticle = await response.json();

        return {
            id: item.id,
            title: item.title,
            summary: item.summary,
            image: item.image_url || "/placeholder.svg",
            category: item.category,
            region: item.region,
            published_at: item.published_at,
            date: formatDate(item.published_at),
            url: item.source_url
        };
    } catch (error) {
        console.error("API Error:", error);
        return null;
    }
};

const months = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
];

function formatDate(isoString: string): string {
    if (!isoString) return "";
    const date = new Date(isoString);
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();
    return `${day} ${month} ${year}`;
}
