import { Router } from "express";
import { listNews, getNewsDetail } from "../../controllers/publicNewsController";

const router = Router();

// GET /v1/news?region=...
router.get("/news", listNews);

// GET /v1/news/:id
router.get("/news/:id", getNewsDetail);

export default router;
