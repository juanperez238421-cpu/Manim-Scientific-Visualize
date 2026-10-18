import { defineConfig } from "@playwright/test";

/** Chromium real. En sandbox sin CDN de Playwright, CHROMIUM_PATH apunta a un binario empaquetado por npm. */
const executablePath = process.env.CHROMIUM_PATH || undefined;
export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 90_000,
  retries: 0,
  workers: 1,
  reporter: [["list"], ["json", { outputFile: "qa/e2e-results.json" }]],
  use: {
    baseURL: process.env.WEB_URL ?? "http://127.0.0.1:3000",
    launchOptions: { executablePath, args: ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"] },
    trace: "off",
  },
});
