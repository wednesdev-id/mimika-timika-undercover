import { Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";

interface NewsCardProps {
  id: number;
  title: string;
  date: string;
  summary: string;
  image: string;
}

const NewsCard = ({ id, title, date, summary, image }: NewsCardProps) => {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="relative h-48 overflow-hidden">
        <img
          src={image}
          alt={title}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
        />
      </div>
      
      <CardHeader className="pb-3">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
          <Calendar className="h-4 w-4" />
          <time>{date}</time>
        </div>
        <h3 className="font-semibold text-lg leading-tight line-clamp-2">
          {title}
        </h3>
      </CardHeader>
      
      <CardContent className="pb-3">
        <p className="text-sm text-muted-foreground line-clamp-3">
          {summary}
        </p>
      </CardContent>
      
      <CardFooter>
        <Button variant="news" size="sm" className="w-full">
          Baca Selengkapnya
        </Button>
      </CardFooter>
    </Card>
  );
};

export default NewsCard;
