# PRD: Portal Berita Timika & Mimika Undercover — Core System

## Ringkasan Eksekutif
Produk ini adalah sistem inti (core) yang menjembatani proses scraping berita dari berbagai sumber, normalisasi dan penyimpanan ke PostgreSQL, penyajian data melalui REST API (Express + TypeScript), serta frontend React berbasis palet biru yang konsisten. Dua brand (Timika dan Mimika Undercover) menggunakan core yang sama, dibedakan melalui konfigurasi brand.

## Tujuan Produk & KPI
- Menyediakan portal berita yang selalu terbarui untuk kedua brand.
- Memastikan pipeline scraping → normalisasi → simpan → sajikan stabil dan terukur.
- KPI utama:
  - Latensi API: p95 < 200ms (endpoint list/detail artikel) pada data awal.
  - Keberhasilan job scraping: > 95% tanpa error fatal.
  - Tingkat duplikasi artikel: < 1% setelah dedup.
  - Waktu publish dari sumber → portal: rata-rata < 10 menit.

## Persona & Kebutuhan
- Pembaca (Audience): konsumsi konten cepat, navigasi kategori/tag, pencarian, halaman detail.
- Editor/Operator: memantau job scraping, melihat status sumber, trigger re-scrape manual.
- Admin Teknis: observabilitas (log, metrik), kontrol konfigurasi brand/sumber, penjadwalan job.

## Ruang Lingkup
- In-scope:
  - Scraper modular per situs/brand.
  - Pipelines (normalisasi, dedup, pengelolaan media dasar).
  - Database PostgreSQL dengan Prisma sebagai ORM.
  - REST API untuk artikel, kategori, tag, sumber, job scraping.
  - Frontend portal React dengan palet biru dan routing dasar.
  - Worker untuk pemrosesan antrian (BullMQ/Redis) dan tugas latar belakang.
  - Konfigurasi brand terpusat (nama, logo, tema).
- Out-of-scope (tahap awal):
  - Komentar pengguna, login pembaca, monetisasi iklan.
  - Moderasi konten lanjutan, rekomendasi personalisasi.

## Arsitektur & Alur
- Monorepo: `apps` (frontend), `services` (API & scraper & worker), `packages` (shared: db, ui, types, config, logger, utils), `infra` (docker, scripts).
- Alur data:
  1. Scraper mengambil artikel (HTML/JSON), parse → model artikel.
  2. Pipelines menormalkan, mendeteksi duplikasi, dan memperkaya konten.
  3. Simpan via `packages/db` (Prisma) ke PostgreSQL.
  4. API menyajikan data ke frontend React.
  5. Worker menjalankan job terjadwal, re-scrape, dan tugas latar belakang.

## Struktur Proyek (Monorepo)
Struktur direktori yang disarankan agar scalable dan selaras dengan keputusan dua database terpisah per brand serta dua frontend terpisah.

```plaintext
mimika_timika_undercover/
├── apps/
│   ├── web-timika/                # React + Vite + TS (portal Timika)
│   │   ├── src/
│   │   │   ├── assets/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── routes/
│   │   │   ├── theme/            
│   │   │   │   └── tokens.css      # impor dari packages/ui-tokens
│   │   │   ├── lib/
│   │   │   └── index.tsx
│   │   ├── public/
│   │   ├── vite.config.ts
│   │   └── tsconfig.json
│   └── web-mimika/                # React + Vite + TS (portal Mimika Undercover)
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   ├── routes/
│       │   ├── theme/             # impor tokens CSS
│       │   └── lib/
│       ├── public/
│       ├── vite.config.ts
│       └── tsconfig.json
├── services/
│   ├── api/                # Express + TS, REST API (core)
│   │   ├── src/
│   │   │   ├── app.ts
│   │   │   ├── routes/            # endpoints; dapat dipisah per brand
│   │   │   │   ├── timika/
│   │   │   │   └── mimika/
│   │   │   ├── controllers/
│   │   │   ├── middlewares/
│   │   │   ├── services/
│   │   │   ├── repositories/      # binding ke db per brand
│   │   │   │   ├── timika/
│   │   │   │   └── mimika/
│   │   │   ├── config/
│   │   │   └── healthz.ts
│   │   └── tsconfig.json
│   ├── scraper/                   # pengambilan data dari sumber
│   │   ├── src/
│   │   │   ├── sites/
│   │   │   │   ├── timika/
│   │   │   │   └── mimika-undercover/
│   │   │   ├── parsers/
│   │   │   ├── pipelines/
│   │   │   ├── schedulers/
│   │   │   └── exporters/
│   └── worker/                    # BullMQ/Queue processor
│       ├── src/
│       │   ├── queues/
│       │   │   ├── timika/
│       │   │   └── mimika/
│       │   ├── processors/
│       │   └── config/
├── packages/
│   ├── db-timika/                 # Prisma client untuk timika_db
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   └── migrations/
│   │   └── src/
│   ├── db-mimika/                 # Prisma client untuk mimika_db
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   └── migrations/
│   │   └── src/
│   ├── ui-tokens/                 # CSS variables palet biru
│   │   └── src/theme/tokens.css
│   ├── ui-react/                  # komponen React (wrapper tokens)
│   │   └── src/components/
│   ├── ui-icons/                  # ikon SVG bersama
│   │   └── src/
│   ├── types/                     # shared TypeScript types
│   ├── contracts/                 # antarmuka service/repository
│   ├── config/                    # brand mapping, tsconfig, eslint config
│   │   └── brand.ts
│   ├── sdk/                       # HTTP client (fetch) & util
│   │   └── src/client.ts
│   ├── logger/                    # pino logger
│   └── utils/                     # helpers bersama
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml     # postgres timika/mimika, redis, api, worker, web
│   │   └── Dockerfile.*
│   └── scripts/
│       ├── check-port.sh          # cek & kill port aman (interaktif)
│       └── dev.sh                 # start dengan pengecekan port
├── .env.example                   # variabel lingkungan
├── pnpm-workspace.yaml            # workspace monorepo
├── turbo.json                     # opsional: pipeline task
├── tsconfig.base.json             # shared tsconfig
└── README.md
```

### Konvensi Port (Dev)
- API: `3000`
- Web Timika: `5173`
- Web Mimika: `5174`
- Redis: `6379`
- Postgres: `5432` (opsional DB kedua pada `5433` bila server terpisah)

Sebelum menjalankan aplikasi, selalu cek apakah port sudah dipakai. Jika ya, gunakan port yang sama atau hentikan proses terkait secara aman.

---

## Rencana Migrasi Kode Eksternal → `apps/web-mimika`

Tujuan: memindahkan source code dari proyek eksternal `mimika_dashboard` dan `mimika_landing_page` ke dalam monorepo pada `apps/web-mimika`, menyatukan komponen yang beririsan, dan memastikan aplikasi berjalan di domain `mimikaundercover.com` serta kompatibel dengan core yang sama untuk `timikaundercover.com`.

### Inventaris Awal (Temuan)
- Keduanya berbasis `React + Vite + TypeScript`, memakai stack komponen `shadcn/ui` + `radix-ui` + `tailwindcss`.
- Aliasing: `@` → `./src` (via `vite.config.ts`).
- Tailwind: `tailwind.config.ts` dengan penggunaan CSS variables (`hsl(var(--...))`) dan plugin `tailwindcss-animate`.
- UI lokal: direktori `src/components/ui/*` berisi puluhan komponen shadcn (accordion, button, card, table, dsb.).
- Routing: `react-router-dom@^6`, dashboard memiliki halaman admin (Dashboard, ScrapedNews, VerifiedNews, Publish, Analytics, Settings), landing memiliki beranda sederhana.
- Data saat ini mock; integrasi API di monorepo dilakukan melalui `@undercover/sdk` (endpoint `/api/articles`).

### Komponen Shared (Target)
- Pindahkan komponen generik dari `src/components/ui/*` ke `packages/ui-react` agar bisa dipakai lintas brand.
  - Struktur disarankan: `packages/ui-react/src/shadcn/*` dan ekspor via `packages/ui-react/src/index.ts`.
  - Khusus komponen layout brand (mis. `AdminLayout`, `AdminSidebar`, `Header`, `Footer`) tetap di `apps/*` masing-masing, namun ekstrak bagian generik (mis. `NavLink`, `StatusBadge`) ke shared bila tidak bergantung pada brand.
- Sinkronkan tema/tokens:
  - `packages/ui-tokens/src/theme/tokens.css` menjadi satu sumber CSS variables.
  - Di `apps/web-mimika/src/theme/global.css`, `@import "@undercover/ui-tokens/theme/tokens.css"` sudah ada; tambahkan layer Tailwind di `src/index.css` untuk util kelas.

### Dependensi yang Perlu Ditambahkan di `apps/web-mimika`
- UI & util: `@radix-ui/*`, `class-variance-authority`, `clsx`, `cmdk`, `date-fns`, `embla-carousel-react`, `lucide-react`, `react-hook-form`, `react-resizable-panels`, `sonner`, `tailwind-merge`, `tailwindcss-animate`, `vaul`, `zod`.
- Styling: `tailwindcss`, `postcss`, `autoprefixer`, `@tailwindcss/typography`.
- Dev: `@types/react`, `@types/react-dom`, `@types/node`, `eslint` (opsional; ikuti policy monorepo), plugin Vite.
- Catatan: monorepo saat ini memakai `@vitejs/plugin-react`; opsi untuk beralih ke `@vitejs/plugin-react-swc` jika diinginkan, namun tidak wajib.

### Penyesuaian Konfigurasi
- `vite.config.ts` di `apps/web-mimika`:
  - Tambah alias `@: path.resolve(__dirname, "./src")` agar kompatibel impor.
  - Pertahankan `server.port: 5174` dan proxy `/api → http://localhost:3000`.
- `tailwind.config.ts` di `apps/web-mimika`:
  - Tambahkan `content` mencakup `./src/**/*.{ts,tsx}`.
  - Definisikan warna/tema `hsl(var(--...))` selaras dengan tokens. Atau buat mapping util untuk mengonversi tokens hex ke `--primary`, `--secondary`, dsb.
- `postcss.config.js`: plugin `tailwindcss` dan `autoprefixer`.
- `src/index.css`: impor Tailwind base/components/utilities dan variabel CSS.

### Langkah Migrasi (Step-by-step)
1. Siapkan dependensi di `apps/web-mimika` sesuai daftar di atas (PNPM workspace). Jangan menjalankan perintah sampai port diverifikasi bebas.
2. Tambah alias `@` di `apps/web-mimika/vite.config.ts` dan pastikan `strictPort: true` untuk konsisten dengan manajemen port.
3. Buat folder `apps/web-mimika/src/components/ui/` sementara untuk menampung komponen shadcn (jika belum dipindahkan ke `packages/ui-react`). Salin komponen dari kedua proyek, singkronkan duplikasi.
4. Pindahkan util umum (`src/lib/utils.ts` → `packages/utils` atau tetap lokal bila kecil). Saat ini util `cn()` bisa tetap lokal lalu diekstrak kemudian.
5. Pindahkan halaman landing (`mimika_landing_page/src/pages/*`) ke `apps/web-mimika/src/pages/landing/*`. Integrasikan ke router `routes/index.tsx`.
6. Pindahkan halaman admin dashboard (`mimika_dashboard/src/pages/*`) ke `apps/web-mimika/src/pages/admin/*`. Tambahkan `AdminLayout`, `AdminSidebar`, dsb.
7. Integrasi router: definisikan rute `/` (landing) dan `/admin/*` (dashboard) di `apps/web-mimika/src/routes/index.tsx` menggunakan `react-router-dom`.
8. Integrasi API: ganti akses data mock bertahap dengan `@undercover/sdk` (`api.listArticles`, `api.getArticle`), serta tambahkan endpoint lain sesuai model (lihat bagian Model Data di bawah).
9. Styling: aktifkan Tailwind (index.css + tailwind.config.ts), pastikan kelas dari komponen shadcn terdeteksi oleh `content`.
10. QA: jalankan dev (`pnpm --filter @undercover/web-mimika dev`) setelah memastikan port 5174 bebas; uji rute utama dan komponen.

### Multi-domain & Brand
- Domain: `mimikaundercover.com` (brand: `mimika_undercover`) dan `timikaundercover.com` (brand: `timika`).
- Strategi brand di frontend:
  - `apps/web-*/src/lib/brand.ts` dapat membaca `import.meta.env.VITE_BRAND` atau memetakan `location.hostname` → brand.
  - Pastikan `@undercover/sdk` menerima `brand` sebagai parameter untuk semua pemanggilan.
- Backend/CORS:
  - Pastikan API menerima query `brand` dan mengizinkan CORS dari kedua domain.
  - Proxy dev: `vite.config.ts` sudah memetakan `/api` ke `http://localhost:3000`.

### Model Data Backend (Rinci)
- Entitas yang digunakan (diselaraskan dengan `packages/types` dan perluasan):
  - `Article { id, source_id, brand, title, slug?, excerpt?, content?, cover_image_url?, author?, published_at?, status }`
    - `status`: `pending | verified | hoax | published` (tambahkan kolom ini di types & DB)
  - `Source { id, name, url, brand, active }`
  - `Category { id, name, slug }` dan relasi `ArticleCategory`
  - `Tag { id, name, slug }` dan relasi `ArticleTag`
  - `ScrapeJob { id, name, brand, schedule_cron, active }`
  - `ScrapeRun { id, job_id, started_at, finished_at, status, items_found, items_saved, error }`
- Endpoint minimal untuk frontend:
  - `GET /api/articles?brand=...&q?&category?&tag?&page?&limit?`
  - `GET /api/articles/:id?brand=...`
  - `GET /api/categories`, `GET /api/tags`, `GET /api/sources`
  - `POST /api/scrape/run { brand, sourceId? }`

---

## Skema Database — Timika (Portal Publik)

- Tabel inti (brand: `timika`):
  - `articles_public`
    - `id UUID PK`
    - `brand TEXT CHECK (brand = 'timika')`
    - `source_id UUID NULL` (opsional; referensi ke `sources` di skema mimika)
    - `title TEXT NOT NULL`
    - `slug TEXT NOT NULL UNIQUE` (unik per brand)
    - `excerpt TEXT`
    - `content TEXT`
    - `cover_image_url TEXT`
    - `author TEXT`
    - `published_at TIMESTAMPTZ`
    - `seo_title TEXT` / `seo_description TEXT`
    - `views INT DEFAULT 0`, `likes INT DEFAULT 0`, `trending_score FLOAT DEFAULT 0`
    - `created_at TIMESTAMPTZ DEFAULT now()`, `updated_at TIMESTAMPTZ DEFAULT now()`
  - `categories`
    - `id UUID PK`, `name TEXT UNIQUE`, `slug TEXT UNIQUE`
  - `article_categories`
    - `article_id UUID FK -> articles_public(id)`
    - `category_id UUID FK -> categories(id)`
    - `PRIMARY KEY (article_id, category_id)`
  - `tags`
    - `id UUID PK`, `name TEXT UNIQUE`, `slug TEXT UNIQUE`
  - `article_tags`
    - `article_id UUID FK -> articles_public(id)`
    - `tag_id UUID FK -> tags(id)`
    - `PRIMARY KEY (article_id, tag_id)`
  - `media_assets`
    - `id UUID PK`, `brand TEXT CHECK (brand = 'timika')`
    - `file_url TEXT NOT NULL`, `mime TEXT`, `width INT`, `height INT`
    - `created_at TIMESTAMPTZ DEFAULT now()`

- Contoh definisi SQL inti:

```
CREATE TABLE articles_public (
  id UUID PRIMARY KEY,
  brand TEXT NOT NULL CHECK (brand = 'timika'),
  source_id UUID,
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  excerpt TEXT,
  content TEXT,
  cover_image_url TEXT,
  author TEXT,
  published_at TIMESTAMPTZ,
  seo_title TEXT,
  seo_description TEXT,
  views INT DEFAULT 0,
  likes INT DEFAULT 0,
  trending_score DOUBLE PRECISION DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

- Alur frontend terkait:
  - Halaman beranda/daftar artikel menggunakan `GET /api/articles?brand=timika` dan filter kategori/tag.
  - Halaman detail menggunakan `GET /api/articles/:id?brand=timika`.
  - Analytics portal mengambil `views/likes/trending_score` untuk tampilan tren.

## Skema Database — Mimika Undercover (Admin Pipeline)

- Tabel inti (brand: `mimika_undercover`):
  - `sources`
    - `id UUID PK`, `name TEXT`, `url TEXT`, `brand TEXT CHECK (brand = 'mimika_undercover')`, `active BOOLEAN`
    - `parser_config JSONB` (opsional; pola CSS selector/XPath)
  - `scrape_jobs`
    - `id UUID PK`, `name TEXT`, `brand TEXT`, `schedule_cron TEXT`, `active BOOLEAN`
  - `scrape_runs`
    - `id UUID PK`, `job_id UUID FK -> scrape_jobs(id)`, `started_at TIMESTAMPTZ`, `finished_at TIMESTAMPTZ`, `status TEXT`, `items_found INT`, `items_saved INT`, `error TEXT`
  - `scraped_articles`
    - `id UUID PK`, `source_id UUID FK -> sources(id)`, `brand TEXT CHECK (brand = 'mimika_undercover')`
    - `title TEXT`, `slug TEXT`, `excerpt TEXT`, `content TEXT`, `cover_image_url TEXT`
    - `author TEXT`, `url TEXT`, `date_scraped TIMESTAMPTZ DEFAULT now()`
    - `status TEXT CHECK (status IN ('pending','verified','hoax','published'))`
    - `category TEXT`, `thumbnail_url TEXT`
    - `similarity_hash TEXT` (dedup), `raw JSONB` (opsional)
  - `article_verifications`
    - `id UUID PK`, `scraped_article_id UUID FK -> scraped_articles(id)`
    - `decision TEXT CHECK (decision IN ('verified','hoax'))`, `notes TEXT`
    - `verified_by UUID FK -> users_admin(id)`, `verified_at TIMESTAMPTZ DEFAULT now()`
  - `publish_records`
    - `id UUID PK`, `scraped_article_id UUID FK -> scraped_articles(id)`
    - `published_to TEXT CHECK (published_to IN ('timika'))`, `target_article_id UUID` (FK ke `articles_public.id`)
    - `published_at TIMESTAMPTZ DEFAULT now()`
  - `users_admin`
    - `id UUID PK`, `brand TEXT CHECK (brand = 'mimika_undercover')`, `name TEXT`, `email TEXT UNIQUE`, `password_hash TEXT`, `role TEXT CHECK (role IN ('editor','admin'))`, `active BOOLEAN`
    - `created_at TIMESTAMPTZ DEFAULT now()`
  - `settings`
    - `id UUID PK`, `brand TEXT CHECK (brand = 'mimika_undercover')`
    - `auto_publish_verified BOOLEAN DEFAULT false`
    - `hoax_alerts BOOLEAN DEFAULT true`
    - `daily_summary BOOLEAN DEFAULT false`
    - `scrape_interval_minutes INT DEFAULT 30`
    - `max_articles_per_run INT DEFAULT 50`
    - `enable_scraper BOOLEAN DEFAULT true`

- Contoh definisi SQL inti:

```
CREATE TYPE article_status AS ENUM ('pending','verified','hoax','published');

CREATE TABLE scraped_articles (
  id UUID PRIMARY KEY,
  source_id UUID REFERENCES sources(id),
  brand TEXT NOT NULL CHECK (brand = 'mimika_undercover'),
  title TEXT,
  slug TEXT,
  excerpt TEXT,
  content TEXT,
  cover_image_url TEXT,
  author TEXT,
  url TEXT,
  date_scraped TIMESTAMPTZ DEFAULT now(),
  status article_status NOT NULL DEFAULT 'pending',
  category TEXT,
  thumbnail_url TEXT,
  similarity_hash TEXT,
  raw JSONB
);
```

- Alur frontend terkait:
  - `ScrapedNews` memfilter berdasarkan `status` dan pencarian.
  - `ArticleDetail` mengubah `status` via aksi verifikasi/hoax/publish.
  - `VerifiedNews` menampilkan artikel dengan `decision = verified`.
  - `Publish` membuat `publish_records` (bulk) dan menyalin konten ke `articles_public`.
  - `Settings` membaca/menulis `settings` untuk konfigurasi scraper.

---

## Rencana Backend — API, Struktur, Integrasi

- Stack:
  - Node.js + Express (TypeScript), PostgreSQL, Prisma ORM.
  - Redis + BullMQ (opsional) untuk antrean scraping & publish.
  - Pino untuk logging.

- Struktur direktori backend (monorepo):
  - `services/api/src/app.ts` (bootstrap Express, healthz, CORS)
  - `services/api/src/routes/{timika|mimika}/...` (pemisahan brand secara logis)
  - `services/api/src/controllers/*` (logika per endpoint)
  - `services/api/src/repositories/{timika|mimika}/*` (akses DB sesuai schema)
  - `packages/db-timika` dan `packages/db-mimika` (Prisma client per DB)

- Endpoint utama (awal):
  - Timika:
    - `GET /api/articles?brand=timika&q?&category?&tag?&page?&limit?`
    - `GET /api/articles/:id?brand=timika`
    - `GET /api/categories?brand=timika`, `GET /api/tags?brand=timika`
  - Mimika Undercover:
    - `GET /api/undercover/articles?status?&q?&page?&brand=mimika_undercover`
    - `GET /api/undercover/articles/:id?brand=mimika_undercover`
    - `POST /api/undercover/articles/:id/verify { decision: 'verified'|'hoax', notes? }`
    - `POST /api/undercover/articles/:id/publish { targetBrand: 'timika' }`
    - `GET /api/undercover/sources`, `POST /api/undercover/scrape/run { sourceId? }`
    - `GET /api/undercover/settings`, `PUT /api/undercover/settings`
  - Analytics:
    - `GET /api/analytics/articles-by-status?brand=mimika_undercover&period=month`
    - `GET /api/analytics/published?brand=timika&period=week`

- Integrasi frontend:
  - `@undercover/sdk` sudah mendukung `GET /api/articles` & `GET /api/articles/:id` dengan `brand`.
  - Tambahkan method SDK untuk endpoint undercover (verify/publish/list sumber/settings) jika diperlukan.

- Env & konfigurasi:
  - `DATABASE_URL_TIMIKA`, `DATABASE_URL_MIMIKA`
  - `REDIS_URL` (opsional), `PORT=3000`
  - `CORS_ORIGINS=['http://localhost:5173','http://localhost:5174', prod domains]`

- Keamanan & observabilitas:
  - Rate limit, API key internal untuk endpoint `scrape/run`.
  - Audit log untuk aksi verifikasi/publish (opsional tabel `audit_logs`).
  - Healthz dan metrics endpoint.

## Roadmap Teknis (Tahap Awal)

- Minggu 1:
  - Finalisasi schema Prisma untuk `db-timika` dan `db-mimika` sesuai skema di atas.
  - Bootstrap `services/api` dan koneksi ke kedua DB.
  - Implementasi `GET /api/articles` & `GET /api/articles/:id` untuk Timika.
- Minggu 2:
  - Implementasi daftar `undercover/articles` (filter status, pencarian), `verify`, `publish`.
  - Implementasi `settings` CRUD dan `sources` list.
- Minggu 3:
  - Integrasi scraper (eksisting Python) via API atau direct DB (writer minimal ke `scraped_articles`).
  - Tambahkan analitik dasar (aggregasi status bulanan & published mingguan).

Catatan: perluasan `packages/types` dengan `status` dan tipe `ScrapedArticle` akan diselaraskan setelah backend siap.

### Checklist QA Migrasi
- App build & dev berjalan di `5174` setelah cek/killed port (otomatis via skrip).
- Navigasi `/` dan `/admin/*` berfungsi tanpa error.
- Semua komponen shadcn ter-load dan gaya Tailwind aktif.
- SDK memanggil `/api` dan backend merespons dengan data.
- Brand `mimika_undercover` aktif dan mempengaruhi konten/tema sesuai harapan.

### Catatan Implementasi Bertahap
- Fase 1: Salin komponen ke app-level untuk cepat jalan. Fase 2: ekstrak ke `packages/ui-react` agar reusable lintas brand.
- Fase 3: Lengkapi endpoint backend dan tipe di `packages/types` (`status`, relasi kategori/tag).
- Fase 4: Hardening: linting, test unit untuk komponen utama, visual regression (opsional).

---

## Fitur Utama (Fungsional)
- Scraper
  - Modul per situs: `services/scraper/src/sites/{timika|mimika-undercover}`.
  - Pengaturan timeouts, retries, concurrency, backoff.
  - Dukungan Cheerio/Playwright sesuai kebutuhan situs.
- Pipelines
  - Normalisasi konten (judul, excerpt, content, gambar, tanggal).
  - Dedup berdasarkan kombinasi `source_id + slug/url + title fingerprint`.
  - Download metadata gambar (opsional) & validasi mime.
- API Server
  - Endpoint list/detail artikel, kategori, tag, sumber.
  - Endpoint trigger job scraping manual.
  - Pagination, filter, sort standar.
  - Model error konsisten.
- Worker
  - BullMQ/Redis untuk pengelolaan antrian.
  - Proses re-scrape, dedup batch, dan maintenance ringan.
- Frontend (Portal)
  - Halaman: beranda (daftar), detail artikel, kategori, tag, pencarian.
  - Palet biru konsisten, responsif, SEO dasar (meta, OG tags).
  - Pengaturan brand via konfigurasi shared.

## Model Data (Database)
Entitas utama dan kolom garis besar:
- `sources(id, name, url, brand, active, created_at)`
- `articles(id, source_id, brand, title, slug, excerpt, content, cover_image_url, author, published_at, status, created_at, updated_at)`
- `categories(id, name, slug)`
- `article_categories(article_id, category_id)`
- `tags(id, name, slug)`
- `article_tags(article_id, tag_id)`
- `images(id, article_id, url, width, height, mime_type)`
- `scrape_jobs(id, name, brand, schedule_cron, active)`
- `scrape_runs(id, job_id, started_at, finished_at, status, items_found, items_saved, error)`
- `scrape_items(id, run_id, source_id, url, status, error_message)`

Indeks disarankan: `articles(slug)`, `articles(published_at DESC)`, `articles(brand)`, `articles(source_id)`.

## API Spesifikasi (High-level)
- `GET /articles`
  - Query: `brand`, `category`, `tag`, `q`, `page`, `limit`, `sort=published_at|title`.
- `GET /articles/:id` atau `/articles/:slug`
- `GET /categories`, `GET /tags`, `GET /sources`
- `POST /scrape/run`
  - Body: `{ brand, sourceId?, options? }`
- Response JSON konsisten, error: `{ code, message, details? }`.

## Konfigurasi Brand & Palet Biru
- Brand via `packages/config/brand.ts`, variabel `BRAND=timika|mimika_undercover`.
- Design tokens (CSS variables) untuk palet biru:

```css
:root {
  --color-primary-900: #0D47A1;
  --color-primary-700: #1976D2;
  --color-primary-500: #2196F3;
  --color-primary-400: #42A5F5;
  --color-bg: #F4F8FB;
  --color-surface: #FFFFFF;
  --color-text-primary: #0A1F44;
  --color-text-secondary: #4A6572;
  --color-success: #2E7D32;
  --color-warning: #ED6C02;
  --color-error: #D32F2F;
}
```

Implementasi di `packages/ui/src/theme/tokens.css` dan helper `colors.ts`.

## Non-Fungsional & Keamanan
- Performa: p95 < 200ms untuk endpoint utama, efisien pagination.
- Skalabilitas: modul scraper per situs, worker untuk skala job.
- Reliabilitas: retry/backoff, idempotensi penyimpanan, health checks.
- Keamanan: sanitasi input, CORS terkontrol, auth untuk endpoint manajemen.
- Observabilitas: logging `pino`, metrik `prom-client` (opsional), tracing (opsional).

## Env Vars & Port
Gunakan `.env` dan `.env.example` (jangan commit data sensitif):
- `NODE_ENV=development|production`
- `PORT_API=3000`
- `PORT_WEB=5173`
- `DATABASE_URL_TIMIKA=postgresql://user:pass@localhost:5432/timika_db`
- `DATABASE_URL_MIMIKA=postgresql://user:pass@localhost:5432/mimika_db`
- `REDIS_URL=redis://localhost:6379`
- `BRAND=timika|mimika_undercover`
- `SCRAPER_CONCURRENCY=5`
- `DEFAULT_SOURCE_TIMEOUT_MS=15000`

Catatan:
- Satu instance backend multi-tenant dapat memilih koneksi DB berdasarkan `brand` atau `BRAND_SCOPE`.
- Alternatif: jalankan dua instance backend, masing-masing menggunakan satu `DATABASE_URL_*` khusus.

Sebelum menjalankan aplikasi, cek apakah port sudah dipakai (3000, 5173, 5432, 6379). Jika sudah, gunakan port yang sama atau hentikan proses terkait secara aman.

## UX & Halaman Frontend
- Beranda: daftar artikel, filter brand/kategori/tag, pencarian.
- Detail artikel: judul, tanggal, penulis, konten, gambar, tag.
- Kategori & Tag: listing dan navigasi.
- Sumber: daftar sumber dengan status aktif.
- SEO dasar: meta, OG tags, sitemap (opsional), robots.txt.

## Strategi Frontend Terpisah per Brand
Untuk mengakomodasi perbedaan tampilan, narasi, dan kebutuhan konten antara Timika dan Mimika Undercover, frontend akan dipisah menjadi dua aplikasi berbeda namun berbagi core yang sama.

### Struktur Apps (Disarankan)
- `apps/web-timika` → Portal Timika.
- `apps/web-mimika` → Portal Mimika Undercover.

Keduanya menggunakan paket bersama:
- `packages/ui` (design system palet biru, komponen bersama).
- `packages/config` (brand tokens: nama, logo, warna, copywriting).
- `packages/types`, `packages/utils`, `packages/logger` (tooling shared).

### Integrasi dengan Backend
- Backend core tetap satu (multi-tenant) dengan filter `brand` di semua endpoint.
- Opsi deploy: satu instance backend untuk keduanya atau dua instance dengan `BRAND_SCOPE` berbeda (`timika` vs `mimika_undercover`).
- Frontend memanggil endpoint yang sama, menambahkan parameter `brand` atau menggunakan default dari env.

### Konfigurasi & Theming
- Set `BRAND=timika|mimika_undercover` di environment masing-masing apps.
- Theming memakai tokens di `packages/ui/src/theme/tokens.css` dan mapping di `packages/config/brand.ts`.
- Perbedaan elemen statis (logo, tagline, footer links) dikendalikan melalui konfigurasi brand.

## Strategi Model Per Brand (Core Sama, Model Beda)
Karena peruntukan berbeda, model data/DTO per brand dapat berbeda meskipun backend core sama. Pendekatan ini menjaga shared core (controllers, services, middlewares, error model) namun memberi kebebasan domain per brand.

### Prinsip
- Core berbagi kontrak antarmuka (service & repository) dan error model.
- Domain per brand didefinisikan sebagai paket/ modul terpisah yang mengimplementasikan kontrak shared.
- API dapat memaparkan respons berbeda per brand, namun tetap konsisten pada pola pagination, status code, dan error wrapper.

### Opsi Desain Database
- Opsi A — Satu database, skema Postgres per brand:
  - `schema timika` dan `schema mimika_undercover` untuk memisahkan tabel dan migrasi.
  - Dua Prisma client di paket terpisah: `packages/db-timika` dan `packages/db-mimika`.
  - Kelebihan: isolasi skema, migrasi per brand lebih aman; kekurangan: dua set migrasi.

```prisma
// packages/db-timika/prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  schema   = "timika"
}

// packages/db-mimika/prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  schema   = "mimika_undercover"
}
```

- Opsi B — Satu skema dengan superset kolom + kolom `brand`:
  - Sederhana untuk query gabungan, namun kolom opsional bisa tumbuh kompleks.
  - Cocok jika perbedaan model kecil/menengah.

- Opsi C — Dua database berbeda:
  - Isolasi kuat; cocok untuk SLA/kompliance berbeda; biaya operasional lebih tinggi.

### Keputusan: Menggunakan Dua Database Terpisah per Brand
- Setiap brand menggunakan database PostgreSQL sendiri: `timika_db` dan `mimika_db`.
- Prisma client dikelola per brand (mis.: `packages/db-timika` dan `packages/db-mimika`).
- Backend core dapat berjalan sebagai satu proses multi-tenant (memilih koneksi DB berdasarkan `brand`) atau dua proses terpisah (masing-masing bound ke satu DB dengan `BRAND_SCOPE`).
- Migrations, backup, dan monitoring dijalankan per database untuk isolasi penuh.

### Kontrak Domain & Repositori
- Definisikan kontrak generik di `packages/contracts` (shared):

```ts
export interface ArticleRepository<TArticle> {
  findMany(params: FindParams): Promise<TArticle[]>;
  findById(id: string): Promise<TArticle | null>;
  create(input: TArticleInput): Promise<TArticle>;
}

export interface ArticleService<TArticleDTO> {
  list(params: ListParams): Promise<Paginated<TArticleDTO>>;
  get(idOrSlug: string): Promise<TArticleDTO | null>;
}
```

- Implementasi per brand berada di `packages/domain/timika` dan `packages/domain/mimika` yang mengikat ke Prisma client masing-masing (atau mapper superset).
- Mapping DTO per brand memproyeksikan field yang relevan untuk frontend tersebut.

### API & Versi
- Opsi path per brand: `/timika/articles` dan `/mimika/articles` (jelas dan eksplisit).
- Alternatif query/header: `GET /articles?brand=timika` atau header `X-Brand: timika`.
- OpenAPI dapat memiliki dua skema respons atau satu skema dengan discriminated union berbasis `brand`.

### Scraper & Worker
- Scraper menghasilkan model mentah per brand; pipeline shared menormalkan dan melakukan dedup sesuai aturan brand.
- Queue dipisah per brand: `queue:articles:timika` dan `queue:articles:mimika` untuk isolasi job.

### Testing & Migrasi
- Unit test per brand untuk parser/pipeline; integrasi test mengacu ke Prisma client/ skema yang sesuai.
- Migrasi dikelola per paket DB (Opsi A) atau satu migrasi superset (Opsi B).

### Rekomendasi Awal
- Mulai dengan Opsi A (skema terpisah per brand) jika perbedaan model cukup besar; memberi ruang evolusi tanpa kompromi.
- Jika perbedaan kecil, Opsi B dapat diterapkan untuk kesederhanaan awal.

### Acceptance Tambahan
- Endpoint per brand mengembalikan DTO sesuai desain masing-masing, namun pagination, status code, dan error wrapper konsisten.
- Migrasi berjalan terpisah tanpa saling mengganggu antar brand (untuk Opsi A).

## Variasi Framework Frontend dalam Monorepo
Monorepo ini dapat menampung dua frontend dengan framework berbeda (misal: React Vite untuk Timika, Next.js atau Astro untuk Mimika Undercover) tanpa masalah signifikan, asalkan core dibangun framework-agnostic.

### Prinsip Desain
- Framework-agnostic di layer shared: design tokens (CSS variables), types/DTO, contracts API, config brand.
- Wrapper per framework untuk komponen: `ui-react`, `ui-web` (web components) atau `ui-vue` bila diperlukan.
- SDK HTTP (fetch client) tanpa ketergantungan framework: `packages/sdk` untuk akses API.

### Paket Shared yang Direkomendasikan
- `packages/ui-tokens` → CSS variables palet biru dan spacing/typography.
- `packages/ui-icons` → set SVG ikon bersama.
- `packages/ui-react` → komponen React yang memanfaatkan tokens.
- `packages/ui-web` (opsional) → web components (Lit/Stencil) agar lintas framework.
- `packages/types` → tipe/DTO bersama.
- `packages/contracts` → antarmuka service/repository.
- `packages/config` → brand mapping (nama, logo, warna, copy).
- `packages/sdk` → client API (fetch), util retry/caching.

### Contoh Struktur Apps
- `apps/web-timika` (React + Vite)
- `apps/web-mimika` (Next.js atau Astro + React islands)

Keduanya mengimpor dari paket shared di atas sehingga theming, tipe, dan kontrak tetap konsisten.

### Build & CI
- Gunakan pnpm workspace + (opsional) Turborepo untuk pipeline lint/build/test per app.
- Konfigurasi task per framework (Vite/Next/Astro) dengan cache terpisah, tetap dalam satu orkestrasi monorepo.

### Risiko & Mitigasi
- Duplikasi bundle antar apps: pastikan packages di-build sebagai library ESM/CJS yang tree-shakable.
- Perbedaan SSR/CSR: definisikan batas di level halaman; komponen UI dibuat stateless sebisa mungkin dan hindari side-effect global.
- Styling konsisten: tokens di-load global; framework-specific wrapper hanya untuk interaksi, bukan warna/spacing.

### Rekomendasi MVP
- Untuk kecepatan, mulai dengan React di kedua apps; jika ingin beda framework, pastikan `ui-tokens`, `types`, `contracts`, dan `sdk` rampung dulu.
- Pastikan cek port dev server per app: `PORT_WEB_TIMIKA=5173`, `PORT_WEB_MIMIKA=5174` (atau default framework), dan gunakan script pengecekan port sebelum run.

## Roadmap & Milestone
1. Setup monorepo (apps, services, packages, infra), tsconfig, lint.
2. Prisma schema & migrasi awal untuk dua DB (`packages/db-timika` dan `packages/db-mimika`).
3. API dasar: `GET /articles`, `GET /sources` + health check.
4. Scraper MVP untuk 1–2 sumber tiap brand.
5. Frontend MVP terpisah: `apps/web-timika` dan `apps/web-mimika` (daftar & detail, palet biru aktif, konfigurasi brand).
6. Worker: dedup, re-scrape terjadwal, monitoring sederhana; queue terpisah per brand.
7. Admin panel (opsional): status job & trigger manual.

## Kriteria Penerimaan (Acceptance Criteria)
- Scraper mampu mengambil minimal 20 artikel dari 1 sumber/brand dalam 1 jam tanpa error fatal.
- Data tersimpan konsisten dan dapat diakses via API list/detail.
- Frontend menampilkan daftar & detail dengan palet biru konsisten lintas brand.
- Port pengecekan dilakukan sebelum proses run (dev scripts atau manual), tanpa konflik.

## Risiko & Mitigasi
- Perubahan struktur HTML sumber: gunakan parser modular + tes unit.
- Blokir IP atau rate-limit: atur concurrency, retry backoff, user-agent rotation.
- Duplikasi tinggi: fingerprint judul + canonical URL + hash konten.
- Pertumbuhan DB: indeks tepat, pembersihan media, archiving.
- SEO: perhatikan meta & OG tags, sitemap, canonical.

## Testing & QA
- Unit: parsers, pipelines (normalisasi/dedup).
- Integrasi: repositories, API endpoints.
- E2E ringan: alur scrape → simpan → tampil.
- Smoke test pasca deploy; load test dasar untuk list artikel.

## Operasional & Observabilitas
- Logging terstruktur (pino) dengan level per environment.
- Health checks: `/healthz` API, konektivitas DB/Redis.
- Backups per database (timika_db dan mimika_db) & rencana rollback migrasi terpisah.
- Alerting sederhana (opsional) untuk job gagal beruntun.

## Lampiran
- Struktur folder (high-level) disarankan ada di README.
- Contoh `.env.example` akan disertakan di root proyek.
- Skrip `infra/scripts/check-port.sh` untuk pengecekan/kill port aman (interaktif).