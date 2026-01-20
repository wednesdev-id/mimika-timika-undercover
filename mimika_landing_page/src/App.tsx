import { Toaster as Sonner } from "@/shared/ui";
import { TooltipProvider } from "@/shared/ui";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Index from "./pages/Index";
import Dashboard from "./pages/Dashboard";
import ScrapedNews from "./pages/ScrapedNews";
import ArticleDetail from "./pages/ArticleDetail";
import VerifiedNews from "./pages/VerifiedNews";
import Publish from "./pages/Publish";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";
import LatestNews from "./pages/LatestNews";
import About from "./pages/About";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/scraped-news" element={<ScrapedNews />} />
          <Route path="/berita-terbaru" element={<LatestNews />} />
          <Route path="/tentang" element={<About />} />
          <Route path="/article/:id" element={<ArticleDetail />} />
          <Route path="/verified-news" element={<VerifiedNews />} />
          <Route path="/publish" element={<Publish />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
