
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

interface CategoryPopupProps {
    isOpen: boolean;
    onClose: () => void;
}

const categories = [
    "Ekonomi",
    "Hukum & Kriminal",
    "Pemerintahan",
    "Sosial & Budaya",
    "Pendidikan",
    "Kesehatan",
    "Lingkungan",
    "Olahraga",
    "Opini",
];

const CategoryPopup = ({ isOpen, onClose }: CategoryPopupProps) => {
    const navigate = useNavigate();

    if (!isOpen) return null;

    const handleCategoryClick = (category: string) => {
        navigate(`/berita-terbaru?category=${encodeURIComponent(category)}`);
        onClose();
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-in fade-in duration-200">
            <div className="relative w-full max-w-lg rounded-lg bg-card p-6 shadow-xl border animate-in zoom-in-95 duration-200">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold">Pilih Kategori</h2>
                    <Button variant="ghost" size="icon" onClick={onClose} className="h-8 w-8 rounded-full">
                        <X className="h-4 w-4" />
                    </Button>
                </div>

                <div className="grid grid-cols-2 gap-3">
                    {categories.map((category) => (
                        <Button
                            key={category}
                            variant="outline"
                            className="justify-start h-auto py-3 px-4 text-left hover:bg-primary/5 hover:border-primary transition-colors"
                            onClick={() => handleCategoryClick(category)}
                        >
                            <span className="truncate">{category}</span>
                        </Button>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CategoryPopup;
