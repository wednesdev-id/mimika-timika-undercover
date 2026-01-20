// Minimal stub untuk tipe Express agar kompilasi TypeScript tidak error.
// Catatan: Ini hanya untuk menghilangkan error tipe. Untuk runtime,
// Anda tetap perlu menginstal paket "express" sebenarnya.

declare module "express" {
  export interface Request {
    query: any;
    params: any;
    body: any;
  }

  export interface Response {
    status(code: number): Response;
    json(body: any): Response;
  }

  export interface Router {
    use(...args: any[]): Router;
    get(path: string, handler: any): Router;
    post(path: string, handler: any): Router;
    put(path: string, handler: any): Router;
    delete(path: string, handler: any): Router;
  }

  export interface Application {
    use(...args: any[]): void;
    get(path: string, handler: any): any;
    post(path: string, handler: any): any;
    put(path: string, handler: any): any;
    delete(path: string, handler: any): any;
    listen(port: number, cb?: (...args: any[]) => void): any;
  }

  export interface Express {
    (): Application;
    Router(): Router;
    json(): any;
  }

  // Named value exports agar `import { Router } from "express"` bekerja
  export function Router(): Router;
  export function json(): any;

  const express: Express;
  export default express;
}
