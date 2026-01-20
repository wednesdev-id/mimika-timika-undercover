import { Request, Response } from "express";
import { Settings } from "@undercover/types";
import { MimikaSettingsRepo } from "../../repositories/mimika/settingsRepo";
import { z } from "zod";

export async function getSettings(_req: Request, res: Response) {
  const repo = new MimikaSettingsRepo();
  const data = await repo.get();
  res.json({ data });
}

export async function updateSettings(req: Request, res: Response) {
  const body = z.object({ settings: z.array(z.object({ key: z.string(), value: z.any() })) }).parse(req.body ?? {});
  const repo = new MimikaSettingsRepo();
  const data = await repo.update(body.settings as Settings[]);
  res.json({ data });
}
