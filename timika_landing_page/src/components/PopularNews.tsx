import { TrendingUp } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import news1 from "@/assets/news-1.jpg";
import news2 from "@/assets/news-2.jpg";
import news3 from "@/assets/news-3.jpg";
import news4 from "@/assets/news-4.jpg";
import news5 from "@/assets/news-5.jpg";

interface PopularNewsItem {
  id: number;
  title: string;
  date: string;
  image: string;
}

const popularNewsData: PopularNewsItem[] = [
  {
    id: 1,
    title: "Pembangunan Infrastruktur Timika Dipercepat Tahun Ini",
    date: "15 Jan 2025",
    image: news1
  },
  {
    id: 2,
    title: "Festival Budaya Papua Akan Digelar di Mimika",
    date: "14 Jan 2025",
    image: news2
  },
  {
    id: 3,
    title: "Peningkatan Kualitas Pendidikan di Wilayah Papua",
    date: "13 Jan 2025",
    image: news3
  },
  {
    id: 4,
    title: "Program Kesehatan Gratis untuk Masyarakat Timika",
    date: "12 Jan 2025",
    image: news4
  },
  {
    id: 5,
    title: "Pelestarian Hutan Papua Mendapat Dukungan Internasional",
    date: "11 Jan 2025",
    image: news5
  }
];

const PopularNews = () => {
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
          {popularNewsData.map((news, index) => (
            <li key={news.id} className="border-b last:border-0 pb-4 last:pb-0">
              <a href="#" className="flex gap-3 group">
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
