export interface NewsArticle {
    id: number;
    title: string;
    source: string;
    date: string;
    category: string;
    image: string;
    likes: number;
    comments: number;
    summary?: string;
}

const API_BASE_URL = "/api/public/v1";

interface ApiResponse {
    data: any[];
    meta: any;
}

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

export const fetchNews = async (region: "mimika" | "timika", category?: string): Promise<NewsArticle[]> => {
    const params = new URLSearchParams();
    params.append("region", region);
    if (category) params.append("category", category);

    try {
        const response = await fetch(`${API_BASE_URL}/news?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch news");

        const json: ApiResponse = await response.json();

        // Map Backend Response to Frontend Interface
        return json.data.map((item: any) => ({
            id: item.id,
            title: item.title,
            source: "Timika News Portal", // Default source if not in API, or map from item.source if available
            date: formatDate(item.published_at),
            summary: item.summary,
            image: item.image_url || "/placeholder.jpg",
            category: item.category,
            likes: 0, // Default as API might not return this yet
            comments: 0 // Default
        }));
    } catch (error) {
        console.error("API Error:", error);
        return [];
    }
};
