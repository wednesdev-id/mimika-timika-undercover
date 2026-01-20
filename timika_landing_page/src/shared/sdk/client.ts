import type {
  BrandKey,
  Article,
  ScrapedArticle,
  ArticleStatus,
  Settings,
  Source,
  PublishRecord,
  ArticleVerification,
} from "@undercover/types";

const BASE = "/api";
const UNDERCOVER = "/api/undercover";

export async function getArticles(brand: BrandKey): Promise<Article[]> {
  const res = await fetch(`${BASE}/articles?brand=${brand}`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as Article[];
}

export async function getArticle(brand: BrandKey, id: string): Promise<Article> {
  const res = await fetch(`${BASE}/articles/${id}?brand=${brand}`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as Article;
}

// Undercover: list scraped articles with optional status & pagination
export async function listScrapedArticles(params: {
  status?: ArticleStatus;
  page?: number;
  pageSize?: number;
}): Promise<ScrapedArticle[]> {
  const qp = new URLSearchParams();
  if (params.status) qp.set("status", params.status);
  if (params.page !== undefined) qp.set("page", String(params.page));
  if (params.pageSize !== undefined) qp.set("pageSize", String(params.pageSize));
  const res = await fetch(`${UNDERCOVER}/articles?${qp.toString()}`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as ScrapedArticle[];
}

// Undercover: verify article
export async function verifyArticle(
  id: string,
  decision: Exclude<ArticleStatus, "pending" | "published">,
  notes?: string
): Promise<ArticleVerification> {
  const res = await fetch(`${UNDERCOVER}/articles/${id}/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ decision, notes }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as ArticleVerification;
}

// Undercover: publish article
export async function publishArticle(
  id: string,
  opts: { publishAt?: string; targetBrand?: BrandKey } = {}
): Promise<PublishRecord> {
  const res = await fetch(`${UNDERCOVER}/articles/${id}/publish`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ publishAt: opts.publishAt, targetBrand: opts.targetBrand ?? "timika" }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as PublishRecord;
}

// Undercover: settings
export async function getSettings(): Promise<Settings[]> {
  const res = await fetch(`${UNDERCOVER}/settings`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as Settings[];
}

export async function updateSettings(settings: Settings[]): Promise<Settings[]> {
  const res = await fetch(`${UNDERCOVER}/settings`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ settings }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as Settings[];
}

// Undercover: sources
export async function listSources(): Promise<Source[]> {
  const res = await fetch(`${UNDERCOVER}/sources`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as Source[];
}

// Undercover: run scrape
export async function runScrape(sourceId?: string): Promise<{ runId?: string } & Record<string, unknown>> {
  const res = await fetch(`${UNDERCOVER}/scrape/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sourceId }),
  });
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  const json = await res.json();
  return json.data as { runId?: string } & Record<string, unknown>;
}