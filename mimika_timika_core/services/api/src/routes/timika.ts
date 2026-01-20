import { Router } from "express";
import { listArticles, getArticle } from "../controllers/timika/articlesController";

const router = Router();

// Daftar artikel publik
router.get("/articles", listArticles);

// Detail artikel publik
router.get("/articles/:id", getArticle);

export default router;