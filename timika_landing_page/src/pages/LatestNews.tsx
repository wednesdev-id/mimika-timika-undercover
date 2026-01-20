
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Header from "@/components/Header";
import NewsCard from "@/components/NewsCard";
import Footer from "@/components/Footer";
import SearchBar from "@/components/SearchBar";
import { fetchNews } from "@/services/api";
import { NewsArticle } from "@undercover/types";

import { siteConfig } from "@/config/site";

const months: { [key: string]: number } = {
    "Januari": 0, "Februari": 1, "Maret": 2, "April": 3, "Mei": 4, "Juni": 5,
    "Juli": 6, "Agustus": 7, "September": 8, "Oktober": 9, "November": 10, "Desember": 11
};

const parseDate = (dateStr: string) => {
    const parts = dateStr.split(" ");
    if (parts.length !== 3) return new Date();

    const day = parseInt(parts[0], 10);
    const month = months[parts[1]] || 0;
    const year = parseInt(parts[2], 10);

    return new Date(year, month, day);
};

const LatestNews = () => {
    const [news, setNews] = useState<NewsArticle[]>([]);
    const [loading, setLoading] = useState(true);

    const [searchParams] = useSearchParams();
    const categoryParam = searchParams.get("category");

    useEffect(() => {
        const loadNews = async () => {
            setLoading(true);
            try {
                // Fetch for timika region
                const data = await fetchNews("timika", categoryParam || undefined);
                setNews(data);
            } catch (error) {
                console.error("Failed to load news", error);
            } finally {
                setLoading(false);
            }
        };

        loadNews();
    }, [categoryParam]);

    return (
        <div className="min-h-screen flex flex-col">
            <Header />

            <main className="flex-1 container mx-auto px-4 py-8">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-foreground">Berita Terbaru</h1>
                        {categoryParam && (
                            <p className="text-muted-foreground mt-2">
                                Menampilkan kategori: <span className="font-semibold text-primary">{categoryParam}</span>
                            </p>
                        )}
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {loading ? (
                        <div className="col-span-full text-center py-12">Loading...</div>
                    ) : news.length > 0 ? (
                        news.map((article) => (
                            <NewsCard
                                key={article.id}
                                id={article.id}
                                title={article.title}
                                date={article.date}
                                summary={article.summary}
                                image={article.image}
                                url={article.url}
                            />
                        ))
                    ) : (
                        <div className="col-span-full text-center py-12">
                            <p className="text-muted-foreground">
                                Tidak ada berita yang ditemukan{categoryParam ? ` untuk kategori "${categoryParam}"` : ""}.
                            </p>
                        </div>
                    )}
                </div>
            </main>

            <Footer />
        </div>
    );
};

export default LatestNews;
