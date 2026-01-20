import { Request, Response } from "express";
import fetch from "node-fetch";
import { config } from "../config";

const BACKEND_URL = config.BACKEND_SERVICE_URL;

export async function listNews(req: Request, res: Response) {
    try {
        const { region, limit, page, category } = req.query;

        if (!region) {
            return res.status(400).json({
                error: "MISSING_REGION",
                message: "Region parameter is mandatory (mimika/timika)."
            });
        }

        // Build URL params
        const params = new URLSearchParams();
        params.append("region", String(region));
        if (limit) params.append("limit", String(limit));
        // Note: Python backend might not yet support page/category, but we pass them if it does later
        // or we can ignore them for now to match backend strictness

        const response = await fetch(`${BACKEND_URL}/articles?${params.toString()}`);

        if (!response.ok) {
            throw new Error(`Backend responded with ${response.status}`);
        }

        const data = await response.json();

        // Transform to standard contract
        res.json({
            data: data,
            meta: {
                total_items: Array.isArray(data) ? data.length : 0
                // Real pagination requires backend support
            }
        });

    } catch (error) {
        console.error("Proxy Error:", error);
        res.status(502).json({ error: "Backend Service Unavailable" });
    }
}

export async function getNewsDetail(req: Request, res: Response) {
    try {
        const { id } = req.params;

        const response = await fetch(`${BACKEND_URL}/articles/${id}`);

        if (response.status === 404) {
            return res.status(404).json({ error: "Article Not Found" });
        }

        if (!response.ok) {
            throw new Error(`Backend responded with ${response.status}`);
        }

        const data = await response.json();
        res.json({ data });

    } catch (error) {
        console.error("Proxy Error:", error);
        res.status(502).json({ error: "Backend Service Unavailable" });
    }
}
