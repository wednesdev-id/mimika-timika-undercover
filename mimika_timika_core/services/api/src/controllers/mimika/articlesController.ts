import { Request, Response } from "express";
import { ArticleStatus, BrandKey } from "@undercover/types";
import { z } from "zod";
import { MimikaScrapedArticlesRepo } from "../../repositories/mimika/scrapedArticlesRepo";
import { TimikaArticlesRepo } from "../../repositories/timika/articlesRepo";

// Placeholder: implementasikan dengan repositories dari packages/db-mimika
export async function listScrapedArticles(req: Request, res: Response) {
  const qp = z.object({ status: z.enum(["pending", "verified", "hoax", "published"]).optional(), page: z.string().transform((v) => parseInt(v)).optional(), pageSize: z.string().transform((v) => parseInt(v)).optional() }).parse(req.query);
  const repo = new MimikaScrapedArticlesRepo();
  const data = await repo.list(qp.status as ArticleStatus | undefined, qp.page, qp.pageSize);
  res.json({ data });
}

export async function verifyArticle(req: Request, res: Response) {
  const { id } = req.params;
  const body = z.object({ decision: z.enum(["verified", "hoax"]), notes: z.string().optional() }).parse(req.body);
  const repo = new MimikaScrapedArticlesRepo();
  const verification = await repo.verify(id, body.decision, body.notes);
  res.json({ data: verification });
}

export async function publishArticle(req: Request, res: Response) {
  const { id } = req.params;
  const body = z.object({ publishAt: z.string().optional(), targetBrand: z.custom<BrandKey>().optional() }).parse(req.body ?? {});
  const repo = new MimikaScrapedArticlesRepo();
  const record = await repo.publish(id, body.publishAt, body.targetBrand ?? "timika");
  const timika = new TimikaArticlesRepo();
  const scrapedList = await repo.list(undefined);
  const scraped = scrapedList.find((a) => a.id === id);
  if (scraped) await timika.addFromScraped({ id: scraped.id, title: scraped.title, content: scraped.content, cover_image_url: scraped.cover_image_url });
  res.json({ data: record });
}
