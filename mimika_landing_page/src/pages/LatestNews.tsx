
import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Header from "@/components/Header";
import NewsCard from "@/components/NewsCard";
import Footer from "@/components/Footer";
import { newsArticles } from "@/data/newsData";

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
    const [searchParams] = useSearchParams();
    const categoryParam = searchParams.get("category");

    const sortedNews = [...newsArticles].sort((a, b) => {
        return parseDate(b.date).getTime() - parseDate(a.date).getTime();
    });

    const filteredNews = categoryParam
        ? sortedNews.filter(article => {
            // Simple mapping to match mixed case or partial categories if needed
            // For now, strict match or includes
            return article.category.toLowerCase().includes(categoryParam.toLowerCase()) ||
                categoryParam.toLowerCase().includes(article.category.toLowerCase());
        })
        : sortedNews;

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
                    {filteredNews.length > 0 ? (
                        filteredNews.map((article) => (
                            <NewsCard
                                key={article.id}
                                id={article.id}
                                title={article.title}
                                date={article.date}
                                summary={article.summary}
                                image={article.image}
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
