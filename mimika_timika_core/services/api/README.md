# Undercover API Service

Kerangka awal layanan backend untuk Timika (portal publik) dan Mimika Undercover (admin pipeline).

Struktur direktori:

- `src/app.ts` – Inisialisasi Express app dan mount routes.
- `src/routes/timika.ts` – Endpoint publik portal Timika.
- `src/routes/mimika.ts` – Endpoint admin pipeline Mimika Undercover.
- `src/controllers/*` – Handlers per domain (timika/mimika).
- `src/repositories/*` – Abstraksi akses data (placeholder untuk Prisma/SQL).
- `src/config/index.ts` – Konfigurasi environment.

Catatan: Ini adalah kerangka non-eksecutable untuk perencanaan dan integrasi awal. Implementasi repo/DB akan ditambahkan pada fase berikutnya.