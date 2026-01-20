import { Request, Response } from "express";
import { MimikaSourcesRepo } from "../../repositories/mimika/sourcesRepo";

export async function listSources(_req: Request, res: Response) {
  const repo = new MimikaSourcesRepo();
  const data = await repo.list();
  res.json({ data });
}
