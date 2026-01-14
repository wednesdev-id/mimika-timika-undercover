import { Search } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import CategoryPopup from "./CategoryPopup";
import logo from "@/assets/logo-mimika.png";

const Header = () => {
  const [isCategoryPopupOpen, setIsCategoryPopupOpen] = useState(false);

  return (
    <>
      <header className="sticky top-0 z-50 w-full border-b bg-card shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between py-4">
            <Link to="/" className="flex items-center gap-3 group">
              <img
                src={logo}
                alt="Mimika News Portal Logo"
                className="h-12 w-12 object-contain transition-transform group-hover:scale-105"
              />
              <div className="flex flex-col">
                <h1 className="text-2xl font-bold text-primary">Mimika News Portal</h1>
                <p className="text-sm text-muted-foreground">Berita Terbaru dari Mimika</p>
              </div>
            </Link>
          </div>

          <nav className="border-t">
            <ul className="flex flex-wrap gap-6 py-3 text-sm font-medium">
              <li>
                <Link to="/" className="text-foreground hover:text-primary transition-colors">
                  Beranda
                </Link>
              </li>
              <li>
                <Link to="/berita-terbaru" className="text-muted-foreground hover:text-primary transition-colors">
                  Berita Terbaru
                </Link>
              </li>
              <li>
                <button
                  onClick={() => setIsCategoryPopupOpen(true)}
                  className="text-muted-foreground hover:text-primary transition-colors focus:outline-none"
                >
                  Kategori
                </button>
              </li>
              <li>
                <Link to="/tentang" className="text-muted-foreground hover:text-primary transition-colors">
                  Tentang Kami
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>
      <CategoryPopup isOpen={isCategoryPopupOpen} onClose={() => setIsCategoryPopupOpen(false)} />
    </>
  );
};

export default Header;
