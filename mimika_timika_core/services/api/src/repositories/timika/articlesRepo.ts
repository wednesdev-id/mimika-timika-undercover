import { Article, BrandKey } from "@undercover/types";

const publicArticles: Article[] = [
  {
    id: "pub-1",
    source_id: "src-1",
    brand: "timika",
    title: "Program Kesehatan Gratis untuk Warga Timika",
    excerpt: "Dinas Kesehatan Mimika meluncurkan program pemeriksaan kesehatan gratis untuk seluruh warga Timika sepanjang bulan Januari.",
    content: "...",
    cover_image_url: "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400",
    author: "Redaksi",
    published_at: new Date().toISOString(),
    status: "published",
  },
];

export class TimikaArticlesRepo {
  async list(params: { brand?: BrandKey; page?: number; pageSize?: number; category?: string; tag?: string; q?: string }) {
    let data = publicArticles.slice();
    if (params.q) {
      const q = params.q.toLowerCase();
      data = data.filter((a) => (a.title || "").toLowerCase().includes(q) || (a.excerpt || "").toLowerCase().includes(q) || (a.content || "").toLowerCase().includes(q));
    }
    if (params.pageSize && params.page !== undefined) {
      const start = params.page * params.pageSize;
      data = data.slice(start, start + params.pageSize);
    }
    return data;
  }
  async getById(id: string) {
    return publicArticles.find((a) => a.id === id) || null;
  }
  async addFromScraped(scraped: { id: string; title: string; content?: string; cover_image_url?: string }) {
    const art: Article = {
      id: `pub-${scraped.id}`,
      source_id: scraped.id,
      brand: "timika",
      title: scraped.title,
      content: scraped.content,
      cover_image_url: scraped.cover_image_url,
      author: "Admin",
      published_at: new Date().toISOString(),
      status: "published",
    };
    publicArticles.push(art);
    return art;
  }
}
