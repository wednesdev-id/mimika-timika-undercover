import { Router } from "express";
import { listScrapedArticles, verifyArticle, publishArticle } from "../controllers/mimika/articlesController";
import { getSettings, updateSettings } from "../controllers/mimika/settingsController";
import { listSources } from "../controllers/mimika/sourcesController";
import { runScrapeJob } from "../controllers/mimika/scrapeController";

const router = Router();

// Daftar artikel di pipeline (scraped) dengan filter status
router.get("/articles", listScrapedArticles);

// Verifikasi artikel: pending -> verified atau hoax
router.post("/articles/:id/verify", verifyArticle);

// Publish artikel: verified -> published dan pindahkan ke portal publik
router.post("/articles/:id/publish", publishArticle);

// Sumber scraping
router.get("/sources", listSources);

// Jalankan scrape job
router.post("/scrape/run", runScrapeJob);

// Settings Undercover
router.get("/settings", getSettings);
router.put("/settings", updateSettings);

export default router;