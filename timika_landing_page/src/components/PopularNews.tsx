import { useEffect, useState } from "react";
import { TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchNews, NewsArticle } from "../services/api";

const PopularNews = () => {
  const [popularNews, setPopularNews] = useState<NewsArticle[]>([]);

  useEffect(() => {
    const loadNews = async () => {
      const data = await fetchNews();
      // Take first 5 as "popular" for now
      setPopularNews(data.slice(0, 5));
    };
    loadNews();
  }, []);

  return (
    <Card className="sticky top-24">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-lg">
          <TrendingUp className="h-5 w-5 text-primary" />
          Berita Terpopuler
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-4">
          {popularNews.map((news, index) => (
            <li key={news.id} className="border-b last:border-0 pb-4 last:pb-0">
              <a href={news.url} target="_blank" rel="noopener noreferrer" className="flex gap-3 group">
                <span className="flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-primary/10 text-primary font-bold text-sm">
                  {index + 1}
                </span>
                <img
                  src={news.image}
                  alt={news.title}
                  className="flex-shrink-0 w-16 h-16 object-cover rounded-md"
                />
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium leading-tight mb-1 group-hover:text-primary cursor-pointer transition-colors line-clamp-2">
                    {news.title}
                  </h4>
                  <time className="text-xs text-muted-foreground">{news.date}</time>
                </div>
              </a>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};

export default PopularNews;
