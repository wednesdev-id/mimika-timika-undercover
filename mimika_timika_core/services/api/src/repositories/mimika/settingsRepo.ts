import { Settings } from "@undercover/types";

const settingsStore: Settings[] = [
  { key: "portal.name", value: "Timika News Portal" },
  { key: "portal.url", value: "https://timikanews.com" },
  { key: "autopublish.enabled", value: false },
  { key: "notifications.email", value: true },
  { key: "notifications.hoax", value: true },
  { key: "notifications.daily", value: false },
  { key: "scraper.intervalMinutes", value: 30 },
  { key: "scraper.maxArticles", value: 50 },
  { key: "scraper.enabled", value: true },
];

export class MimikaSettingsRepo {
  async get(): Promise<Settings[]> {
    return settingsStore;
  }
  async update(settings: Settings[]): Promise<Settings[]> {
    for (const s of settings) {
      const i = settingsStore.findIndex((x) => x.key === s.key);
      if (i >= 0) settingsStore[i] = { ...settingsStore[i], value: s.value, updated_at: new Date().toISOString() };
      else settingsStore.push({ ...s, updated_at: new Date().toISOString() });
    }
    return settingsStore;
  }
}
