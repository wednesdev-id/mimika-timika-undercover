# Rencana Backend untuk apps/web-mimika

## Ikhtisar
- Tujuan: Mewujudkan backend Express yang sepenuhnya kompatibel dengan frontend `apps/web-mimika`, memakai kontrak dari SDK `@undercover/sdk` dan tipe `@undercover/types`.
- Kondisi saat ini: Struktur backend sudah ada di `services/api` namun semua controller masih `501 Not Implemented`. Database Prisma telah disiapkan di `packages/db-mimika` dan `packages/db-timika`, tetapi belum diintegrasikan.

## Inventaris Frontend & SDK
- Frontend memakai SDK: `apps/web-mimika/src/lib/api.ts:1` → re-export `getArticles`, `getArticle` dari `@undercover/sdk`.
- SDK endpoint basis: `packages/sdk/src/client.ts:12–14` → `BASE = "/api"`, `UNDERCOVER = "/api/undercover"`.
- Endpoint SDK yang perlu didukung:
  - Publik: `GET /api/articles`, `GET /api/articles/:id` (`packages/sdk/src/client.ts:15–27`).
  - Undercover: `GET /api/undercover/articles`, `POST /api/undercover/articles/:id/verify`, `POST /api/undercover/articles/:id/publish`, `GET/PUT /api/undercover/settings`, `GET /api/undercover/sources`, `POST /api/undercover/scrape/run` (`packages/sdk/src/client.ts:29–113`).
- Routing backend sudah sesuai:
  - `services/api/src/app.ts:11–14` → mount `/api` (Timika) & `/api/undercover` (Mimika).
  - `services/api/src/routes/timika.ts:6–10`, `services/api/src/routes/mimika.ts:9–26`.
- Halaman yang akan memakai API (mock saat ini):
  - ScrapedNews `apps/web-mimika/src/pages/ScrapedNews.tsx`, VerifiedNews `.../VerifiedNews.tsx`, ArticleDetail `.../ArticleDetail.tsx`, Publish `.../Publish.tsx`, Settings `.../Settings.tsx`, Index publik `.../Index.tsx`.

## Arsitektur Backend
- Server: Express (TypeScript) di `services/api`.
- Pola: Controller ↔ Repository ↔ Prisma Client.
- Database:
  - Mimika Undercover: `packages/db-mimika/prisma/schema.prisma` (model `ScrapedArticle`, `ArticleVerification`, `PublishRecord`, `Settings`, `Source`).
  - Timika Publik: `packages/db-timika/prisma/schema.prisma` (model `ArticlePublic`, `Category`, `Tag`, `MediaAsset`).
- Response envelope: JSON `{ data, meta? }` dengan status HTTP sesuai; SDK mengharapkan `json.data` (`packages/sdk/src/client.ts:18–20, 25–27, 41–43, 58–59, 73–74, 81–82, 92–93, 100–101, 111–112`).
- Konfigurasi: ENV via `services/api/src/config/index.ts:1–5` (`DATABASE_URL_TIMIKA`, `DATABASE_URL_MIMIKA`, `REDIS_URL`).

## Kontrak API Detail (diselaraskan dengan SDK)
- Publik (Timika):
  - `GET /api/articles?brand=timika&page=&pageSize=&category=&tag=&q=` → kembalikan `Article[]` dari sumber publik (map dari `ArticlePublic`).
  - `GET /api/articles/:id?brand=timika` → detail satu artikel (`Article`).
- Undercover (Mimika):
  - `GET /api/undercover/articles?status=&page=&pageSize=` → `ScrapedArticle[]` dengan filter status dan pagination.
  - `POST /api/undercover/articles/:id/verify` body `{ decision: "verified" | "hoax", notes? }` → buat `ArticleVerification`, ubah status artikel.
  - `POST /api/undercover/articles/:id/publish` body `{ publishAt?, targetBrand? }` → buat `PublishRecord`, salin/transform ke `ArticlePublic` Timika, ubah status `PUBLISHED`.
  - `GET /api/undercover/settings` / `PUT /api/undercover/settings` → CRUD `Settings` berbasis JSON.
  - `GET /api/undercover/sources` → daftar `Source` aktif.
  - `POST /api/undercover/scrape/run` body `{ sourceId? }` → trigger job scraping (awalan: buat `ScrapeRun` dengan `runId`).

## Langkah Implementasi Sistematis
1. Monorepo & Dev Proxy
   - Tambah workspace pattern `services/*` di `pnpm-workspace.yaml` agar backend ikut workspace.
   - Buat `services/api/package.json` (scripts: `dev`, `build`, `start`) dan dependency: `express`, `zod`, `dotenv`, `@prisma/client`, `prisma`, `ts-node-dev`.
   - Vite proxy di `apps/web-mimika/vite.config.ts` → `server.proxy = { "/api": "http://localhost:3000" }` agar `BASE=/api` menuju backend saat dev.
2. Prisma Client & ENV
   - Konfigurasi `.env` root: `DATABASE_URL_TIMIKA`, `DATABASE_URL_MIMIKA`, `REDIS_URL` (opsional).
   - Generate Prisma client untuk kedua DB (`pnpm prisma generate` pada masing-masing package).
3. Repository Implementations
   - `services/api/src/repositories/mimika/*.ts` → implementasi nyata pakai Prisma dari `packages/db-mimika`:
     - `MimikaScrapedArticlesRepo.list(status, page, pageSize)` dengan `orderBy updatedAt desc`.
     - `verify(id, decision, notes)` → transaksi update + insert `ArticleVerification`.
     - `publish(id, publishAt, targetBrand)` → transaksi: insert `PublishRecord`, salin ke Timika.
     - `SourcesRepo.list()` dari model `Source`.
     - `SettingsRepo.get()` / `update(settings)` untuk key-key yang dipakai UI.
   - `services/api/src/repositories/timika/articlesRepo.ts` → implement `list({ page, pageSize, category, tag, q })` dan `getById(id)` dengan Prisma dari `packages/db-timika`.
4. Controller Implementations
   - Isi fungsi di:
     - Mimika: `listScrapedArticles`, `verifyArticle`, `publishArticle`, `listSources`, `getSettings`, `updateSettings`, `runScrapeJob` (`services/api/src/controllers/mimika/*.ts`).
     - Timika: `listArticles`, `getArticle` (`services/api/src/controllers/timika/articlesController.ts:4–20`).
   - Gunakan helper response konsisten: `res.json({ data, meta })` dan penanganan error terpusat.
5. Middleware & Validasi
   - Tambah error handler global dan request validation (Zod) untuk body/query.
   - CORS jika diperlukan (untuk production); dev memakai proxy same-origin.
6. Fitur Batch Publish (opsional)
   - Endpoint tambahan: `POST /api/undercover/articles/publish/batch` body `{ ids: string[], publishAt?, targetBrand? }` untuk mendukung halaman Publish multi-select; atau lakukan loop per-id di frontend tanpa endpoint baru.
7. Seed & Data Awal
   - Script seeding minimal untuk kedua DB agar UI bisa diuji.
8. Testing & QA
   - Uji controller dengan `supertest`/`vitest` untuk endpoint utama.
   - Verifikasi dari frontend: halaman ScrapedNews, VerifiedNews, ArticleDetail, Publish, Settings, Index.

## Todo Kongkrit (siap dieksekusi)
- Tambah `services/*` ke workspace monorepo.
- Buat `services/api/package.json` dan skrip dev/build/start.
- Aktifkan Vite proxy `"/api"` ke backend dev port.
- Generate Prisma client untuk DB Mimika & Timika.
- Implement `MimikaScrapedArticlesRepo` (list, verify, publish).
- Implement `MimikaSettingsRepo` (get/update) & `MimikaSourcesRepo.list`.
- Implement `TimikaArticlesRepo` (list/detail + filter & search).
- Lengkapi semua controller Mimika sesuai kontrak SDK.
- Lengkapi controller Timika `listArticles` dan `getArticle`.
- Tambah helper response dan error middleware.
- Tambah validasi Zod untuk body/query setiap endpoint.
- Opsional: Tambah endpoint batch publish admin.
- Tambah seed scripts untuk DB awal.
- Tambah test endpoint dengan supertest/vitest.

## Verifikasi & Dampak ke Frontend
- Frontend sudah memakai `BASE="/api"` dan `UNDERCOVER="/api/undercover"` sehingga cukup jalankan proxy dev dan backend untuk integrasi.
- Pastikan setiap endpoint mengembalikan `{ data: ... }` agar `json.data` di SDK bekerja (`packages/sdk/src/client.ts:18–20, 25–27, 41–43, 58–59, 73–74, 81–82, 92–93, 100–101, 111–112`).
- Uji aksi utama UI: refresh scraper, verifikasi/hoax, publish, settings save, list/detail publik.

## Catatan Lanjutan
- Autentikasi belum ada di frontend; dapat ditambahkan nanti (JWT + guard route).
- Analytics butuh agregasi tambahan (status bulanan, distribusi sumber); dapat ditambahkan setelah endpoint inti selesai.