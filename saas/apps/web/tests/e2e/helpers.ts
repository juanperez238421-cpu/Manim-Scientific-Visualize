import type { Page } from "@playwright/test";
import path from "node:path";
export const SHOTS = path.join(process.cwd(), "qa", "screenshots");
export const TEST_PDF = process.env.M4_TEST_PDF ?? "";
/** Espera a que terminen las animaciones de entrada antes de capturar. */
export async function settle(page: Page, ms = 3600) { await page.waitForLoadState("networkidle"); await page.waitForTimeout(ms); }
export const shot = (page: Page, name: string, full = true) => page.screenshot({ path: path.join(SHOTS, `${name}.png`), fullPage: full });
