import { Source } from "@undercover/types";

const sources: Source[] = [
  { id: "src-1", name: "Portal Berita Timika", url: "https://timika-portal.example", brand: "mimika_undercover", active: true },
  { id: "src-2", name: "Mimika News", url: "https://mimika-news.example", brand: "mimika_undercover", active: true },
  { id: "src-3", name: "Kompas Papua", url: "https://kompas-papua.example", brand: "mimika_undercover", active: false },
];

export class MimikaSourcesRepo {
  async list(): Promise<Source[]> {
    return sources;
  }
}
