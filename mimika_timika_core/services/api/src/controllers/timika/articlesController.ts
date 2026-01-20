import { Request, Response } from "express";
import { z } from "zod";
import { TimikaArticlesRepo } from "../../repositories/timika/articlesRepo";

export async function listArticles(req: Request, res: Response) {
  const qp = z.object({ page: z.string().transform((v) => parseInt(v)).optional(), pageSize: z.string().transform((v) => parseInt(v)).optional(), category: z.string().optional(), tag: z.string().optional(), q: z.string().optional(), brand: z.string().optional() }).parse(req.query);
  const repo = new TimikaArticlesRepo();
  const data = await repo.list({ page: qp.page, pageSize: qp.pageSize, category: qp.category, tag: qp.tag, q: qp.q, brand: qp.brand as any });
  res.json({ data });
}

export async function getArticle(req: Request, res: Response) {
  const { id } = req.params;
  const repo = new TimikaArticlesRepo();
  const data = await repo.getById(id);
  if (!data) {
    res.status(404).json({ error: "Not Found" });
    return;
  }
  res.json({ data });
}
