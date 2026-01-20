import express from "express";
import type { Request, Response } from "express";
import timikaRouter from "./routes/timika";
import mimikaRouter from "./routes/mimika";
import v1NewsRouter from "./routes/v1/news";

export function createApp() {
  const app = express();
  app.use(express.json());

  // Unified Public API (V1)
  app.use("/public/v1", v1NewsRouter);

  // Legacy/Specific routes (Keep for backward compat or admin)
  app.use("/api", timikaRouter);
  app.use("/api/undercover", mimikaRouter);

  // Health check sederhana
  app.get("/health", (_req: Request, res: Response) => {
    res.json({ status: "ok" });
  });

  return app;
}

export default createApp;