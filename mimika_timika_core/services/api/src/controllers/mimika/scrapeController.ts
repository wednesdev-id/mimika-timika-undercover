import { Request, Response } from "express";
import { config } from "../../config";
import { randomUUID } from "crypto";
import fetch from "node-fetch";

async function tryFetchJson(base: string, paths: string[]): Promise<{ url: string; data: any } | null> {
  for (const p of paths) {
    const url = `${base}/${p}`.replace(/\/+$/, "").replace(/([^:])\/\/+/, "$1/");
    try {
      const res = await fetch(url);
      if (!res.ok) continue;
      const ct = res.headers.get("content-type") || "";
      if (!ct.includes("application/json")) continue;
      const data = await res.json();
      return { url, data };
    } catch (_) {
      continue;
    }
  }
  return null;
}

export async function runScrapeJob(req: Request, res: Response) {
  const { sourceId } = (req.body ?? {}) as { sourceId?: string };
  const base = config.SCRAPER_BASE_URL;
  const candidates = ["api/articles", "articles", "api/news", "news"];
  const result = await tryFetchJson(base, candidates);
  if (!result) {
    res.status(502).json({ data: { runId: randomUUID(), sourceId, fetchedFrom: null, items: [], count: 0 } });
    return;
  }
  const payload: any = result.data;
  const raw = Array.isArray(payload) ? payload : Array.isArray(payload?.data) ? payload.data : [];
  const items = raw.map((it: any) => ({
    id: String(it.id ?? randomUUID()),
    source_id: String(it.source_id ?? sourceId ?? "external"),
    status: "pending",
    title: String(it.title ?? it.name ?? ""),
    content: typeof it.content === "string" ? it.content : JSON.stringify(it.content ?? {}),
    cover_image_url: typeof it.cover_image_url === "string" ? it.cover_image_url : it.image ?? undefined,
    url: typeof it.url === "string" ? it.url : undefined,
    published_at: typeof it.published_at === "string" ? it.published_at : it.publishedAt ?? undefined,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }));
  res.json({ data: { runId: randomUUID(), sourceId, fetchedFrom: result.url, items, count: items.length } });
}
