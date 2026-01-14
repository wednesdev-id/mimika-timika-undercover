import { useState } from "react";
import Header from "@/components/Header";
import SearchBar from "@/components/SearchBar";
import CategoryFilter from "@/components/CategoryFilter";
import NewsCard from "@/components/NewsCard";
import PopularNews from "@/components/PopularNews";
import Footer from "@/components/Footer";
import { newsArticles } from "@/data/newsData";
import heroImage from "@/assets/hero-papua.jpg";

const Index = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("Semua");

  const filteredNews = newsArticles.filter((article) => {
    const matchesSearch =
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.category.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory =
      selectedCategory === "Semua" || article.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      {/* Hero Section */}
      <section className="relative h-[300px] md:h-[400px] overflow-hidden">
        <img
          src={heroImage}
          alt="Papua Landscape"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/40 to-black/20" />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-card px-4">
            <h2 className="text-3xl md:text-5xl font-bold mb-4 drop-shadow-lg">
              Portal Berita Mimika
            </h2>
            <p className="text-lg md:text-xl drop-shadow-md">
              Informasi Terkini dari Tanah Papua
            </p>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="flex-1 container mx-auto px-4 py-8">
        {/* Search Bar */}
        <div className="flex justify-center mb-8">
          <SearchBar onSearch={setSearchQuery} />
        </div>

        {/* Category Filter */}
        <div className="mb-8">
          <CategoryFilter
            selectedCategory={selectedCategory}
            onCategoryChange={setSelectedCategory}
          />
        </div>

        {/* News Grid with Sidebar */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* News Articles */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold mb-6 text-foreground">Berita Terbaru</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                <div className="col-span-2 text-center py-12">
                  <p className="text-muted-foreground">
                    Tidak ada berita yang ditemukan untuk pencarian "{searchQuery}"
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar - Popular News */}
          <aside className="lg:col-span-1">
            <PopularNews />
          </aside>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Index;
