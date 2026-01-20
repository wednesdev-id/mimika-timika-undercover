export const config = {
  DATABASE_URL_TIMIKA: process.env.DATABASE_URL_TIMIKA || "",
  DATABASE_URL_MIMIKA: process.env.DATABASE_URL_MIMIKA || "",
  REDIS_URL: process.env.REDIS_URL || "",
  SCRAPER_BASE_URL: process.env.SCRAPER_BASE_URL || "https://mimika-api.vercel.app",
  BACKEND_SERVICE_URL: process.env.BACKEND_SERVICE_URL || "http://localhost:8000",
};
