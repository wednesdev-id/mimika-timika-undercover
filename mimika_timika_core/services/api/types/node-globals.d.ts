// Deklarasi global minimal untuk proses Node agar TypeScript tidak error.
// Ini hanya untuk kebutuhan typing; tidak mempengaruhi runtime.

declare const process: {
  env: Record<string, string | undefined>;
};