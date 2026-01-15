import { Button } from "@/components/ui/button";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";

interface CategoryFilterProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const categories = [
  "Semua",
  "Politik",
  "Ekonomi",
  "Sosial",
  "Pendidikan",
  "Budaya",
  "Olahraga",
  "Lingkungan"
];

const CategoryFilter = ({ selectedCategory, onCategoryChange }: CategoryFilterProps) => {
  return (
    <div className="w-full mb-8">
      <ScrollArea className="w-full whitespace-nowrap">
        <div className="flex gap-2 pb-4">
          {categories.map((category) => (
            <Button
              key={category}
              onClick={() => onCategoryChange(category)}
              variant={selectedCategory === category ? "default" : "outline"}
              className="rounded-full font-bold shrink-0"
              size="sm"
            >
              {category}
            </Button>
          ))}
        </div>
        <ScrollBar orientation="horizontal" />
      </ScrollArea>
    </div>
  );
};

export default CategoryFilter;
