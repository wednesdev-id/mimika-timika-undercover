import { ArticleStatus, ScrapedArticle, ArticleVerification, PublishRecord, BrandKey } from "@undercover/types";

const store: { articles: ScrapedArticle[]; verifications: ArticleVerification[]; publishes: PublishRecord[] } = {
  articles: [
    {
      id: "1",
      source_id: "src-1",
      status: "pending",
      title: "Pembangunan Jalan Trans Papua Segera Dilanjutkan",
      content: "...",
      cover_image_url: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
      url: "",
      published_at: undefined,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "2",
      source_id: "src-2",
      status: "verified",
      title: "Festival Budaya Mimika Menyambut Tahun 2024",
      content: "...",
      cover_image_url: "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=400",
      url: "",
      published_at: undefined,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: "3",
      source_id: "src-3",
      status: "hoax",
      title: "Hoaks: Klaim Palsu tentang Pertambangan",
      content: "...",
      cover_image_url: "https://images.unsplash.com/photo-1504192010706-dd7f569ee2be?w=400",
      url: "",
      published_at: undefined,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ],
  verifications: [],
  publishes: [],
};

export class MimikaScrapedArticlesRepo {
  async list(status?: ArticleStatus, page?: number, pageSize?: number) {
    let data = store.articles.slice().sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || ""));
    if (status) data = data.filter((a) => a.status === status);
    if (pageSize && page !== undefined) {
      const start = page * pageSize;
      data = data.slice(start, start + pageSize);
    }
    return data;
  }
  async verify(id: string, decision: Exclude<ArticleStatus, "pending" | "published">, notes?: string) {
    const idx = store.articles.findIndex((a) => a.id === id);
    if (idx === -1) throw new Error("Not found");
    store.articles[idx] = { ...store.articles[idx], status: decision, updated_at: new Date().toISOString() };
    const verification: ArticleVerification = {
      id: `${id}-v-${Date.now()}`,
      article_id: id,
      decision,
      notes,
      verified_at: new Date().toISOString(),
      verified_by: "system",
    };
    store.verifications.push(verification);
    return verification;
  }
  async publish(id: string, publishAt?: string, targetBrand: BrandKey = "timika") {
    const idx = store.articles.findIndex((a) => a.id === id);
    if (idx === -1) throw new Error("Not found");
    store.articles[idx] = { ...store.articles[idx], status: "published", published_at: publishAt, updated_at: new Date().toISOString() };
    const record: PublishRecord = {
      id: `${id}-p-${Date.now()}`,
      article_id: id,
      published_at: publishAt || new Date().toISOString(),
      published_by: "system",
      target_brand: targetBrand,
    };
    store.publishes.push(record);
    return record;
  }
}
