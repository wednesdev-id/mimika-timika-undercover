export type BrandKey = "timika" | "mimika_undercover";

export type ArticleStatus = "pending" | "verified" | "hoax" | "published";

export interface Source {
  id: string;
  name: string;
  url: string;
  brand: BrandKey;
  active: boolean;
}

export interface Article {
  id: string;
  source_id: string;
  brand: BrandKey;
  title: string;
  slug?: string;
  excerpt?: string;
  content?: string;
  cover_image_url?: string;
  author?: string;
  published_at?: string;
  status?: ArticleStatus; // opsional untuk kompatibilitas mundur
}

// Artikel hasil scraping untuk pipeline mimika undercover
export interface ScrapedArticle {
  id: string;
  source_id: string;
  status: ArticleStatus; // wajib di pipeline
  title: string;
  content?: string;
  cover_image_url?: string;
  url?: string;
  published_at?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ArticleVerification {
  id: string;
  article_id: string;
  decision: Exclude<ArticleStatus, "pending" | "published">; // verified | hoax
  notes?: string;
  verified_at?: string;
  verified_by?: string;
}

export interface PublishRecord {
  id: string;
  article_id: string;
  published_at: string;
  published_by?: string;
  target_brand: BrandKey;
}

export interface Settings {
  id?: string;
  key: string;
  value: unknown; // bebas (akan disimpan sebagai JSON di DB)
  updated_at?: string;
}

export interface NewsArticle {
  id: number;
  title: string;
  summary: string;
  image: string;
  category: string;
  region: string;
  published_at: string;
  date: string;
  url: string;
}
