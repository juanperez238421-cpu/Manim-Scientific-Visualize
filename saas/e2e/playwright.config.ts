import { defineConfig, devices } from "@playwright/test";
import path from "node:path";
import dotenv from "dotenv";

// Claves de Clerk Development del frontend (NO se imprimen) y rutas del proyecto
dotenv.config({ path: path.resolve(__dirname, "../frontend/.env.local") });
dotenv.config({ path: path.resolve(__dirname, "../.env") });

// H.264 (MP4) solo se reproduce en Chrome/Edge de Google/Microsoft; el Chromium de Playwright NO trae el códec.
const channel = process.env.E2E_BROWSER_CHANNEL || "chrome";

export default defineConfig({
  testDir: "./tests",
  timeout: Number(process.env.E2E_JOB_TIMEOUT_MS || 45 * 60_000) + 120_000,
  expect: { timeout: 20_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  reporter: [["list"], ["html", { open: "never", outputFolder: "../storage/evidence/playwright-report" }]],
  outputDir: "../storage/evidence/playwright-artifacts",
  use: { baseURL: process.env.E2E_BASE_URL || "http://localhost:3000", trace: "retain-on-failure", screenshot: "on", video: "retain-on-failure" },
  projects: [
    { name: "setup", testMatch: /global\.setup\.ts/ },
    { name: "desktop", testMatch: /full-flow\.spec\.ts/, dependencies: ["setup"], use: { ...devices["Desktop Chrome"], channel, viewport: { width: 1440, height: 900 }, acceptDownloads: true } },
    { name: "mobile", testMatch: /mobile\.spec\.ts/, dependencies: ["desktop"], use: { ...devices["Pixel 7"], channel } },
  ],
});
