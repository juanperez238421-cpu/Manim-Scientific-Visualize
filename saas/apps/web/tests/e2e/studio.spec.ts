import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import fs from "node:fs";
import { settle, shot, TEST_PDF } from "./helpers";

test.describe("Studio (backend FastAPI real)", () => {
  test("panel: datos reales de /v1/me y saldo", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/studio");
    await expect(page.getByText("API conectada")).toBeVisible();
    await expect(page.getByText("Sin créditos: no se pueden crear trabajos")).toBeVisible();
    await expect(page.getByText("Entorno de demostración").first()).toBeVisible();
    await settle(page, 500);
    await shot(page, "05-studio-dashboard", false);
  });

  test("error de red: la API caída se informa sin romper la UI", async ({ page }) => {
    await page.route("http://127.0.0.1:8000/**", (r) => r.abort());
    await page.goto("/studio");
    await expect(page.getByText("No hay conexión con la API")).toBeVisible();
    await shot(page, "06-studio-network-error", false);
  });

  test("PDF inválido (texto renombrado .pdf) se rechaza antes de subir", async ({ page }) => {
    await page.goto("/studio/new");
    await expect(page.getByText("API conectada")).toBeVisible();
    await page.getByTestId("pdf-input").setInputFiles({ name: "falso.pdf", mimeType: "application/pdf", buffer: Buffer.from("esto no es un pdf") });
    await expect(page.getByText("cabecera %PDF- ausente")).toBeVisible();
    await shot(page, "07-studio-invalid-pdf", false);
  });

  test("flujo completo con 3.pdf: carga, ejercicios, selección #1, cotización, creación bloqueada", async ({ page }) => {
    test.skip(!TEST_PDF || !fs.existsSync(TEST_PDF), "M4_TEST_PDF no definido");
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/studio/new");
    await expect(page.getByText("API conectada")).toBeVisible();
    await shot(page, "08-studio-new-empty", false);

    await page.getByTestId("pdf-input").setInputFiles(TEST_PDF);
    await expect(page.getByText("Ejercicios detectados (10)")).toBeVisible({ timeout: 60_000 });
    await expect(page.getByText("Carga y validación en el backend")).toBeVisible();
    await expect(page.getByText("status=analyzed · 1 pág.")).toBeVisible();
    await expect(page.getByText("El endpoint no existe aún (M3-D)")).toBeVisible();
    for (let i = 1; i <= 10; i++) await expect(page.getByTestId(`ex-${i}`)).toBeVisible();
    await shot(page, "09-studio-analysis-exercises");

    await page.getByTestId("ex-1").check();
    await page.getByTestId("quote-btn").click();
    await expect(page.getByTestId("backend-estimate")).toBeVisible({ timeout: 30_000 });
    await expect(page.getByTestId("sdi-quote")).toBeVisible({ timeout: 60_000 });
    await expect(page.getByTestId("backend-estimate")).toContainText("39");
    await expect(page.getByTestId("backend-estimate")).toContainText("insuficiente");
    await expect(page.getByTestId("sdi-quote")).toContainText("20");
    await expect(page.getByTestId("sdi-quote")).toContainText("Informativa");
    await expect(page.getByTestId("create-job")).toBeDisabled();
    await expect(page.getByText("Creación de trabajos deshabilitada")).toBeVisible();
    await shot(page, "10-studio-quote-full");

    // la cotización queda invalidada al cambiar la selección (no hay cotizaciones obsoletas)
    await page.getByTestId("ex-2").check();
    await expect(page.getByTestId("sdi-quote")).toHaveCount(0);
    await page.getByTestId("ex-2").uncheck();

    // el backend no creó trabajos
    await page.goto("/studio/jobs");
    await expect(page.getByText("Aún no hay trabajos")).toBeVisible();
    await shot(page, "11-studio-history-empty", false);
  });

  test("móvil: flujo de análisis legible", async ({ page }) => {
    test.skip(!TEST_PDF || !fs.existsSync(TEST_PDF), "M4_TEST_PDF no definido");
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/studio/new");
    await expect(page.getByText("API conectada")).toBeVisible();
    await page.getByTestId("pdf-input").setInputFiles(TEST_PDF);
    await expect(page.getByText("Ejercicios detectados (10)")).toBeVisible({ timeout: 60_000 });
    await page.getByTestId("ex-1").check();
    await page.getByTestId("quote-btn").click();
    await expect(page.getByTestId("sdi-quote")).toBeVisible({ timeout: 60_000 });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(0);
    await shot(page, "12-studio-mobile-flow");
  });

  test("trabajo inexistente: 404 explícito", async ({ page }) => {
    await page.goto("/studio/jobs/00000000-0000-0000-0000-000000000000");
    await expect(page.getByText("Trabajo no encontrado")).toBeVisible();
  });

  test("estado del sistema: capacidades y llamadas reales", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/studio/status");
    await expect(page.getByText("Autenticación Clerk")).toBeVisible();
    await expect(page.getByRole("cell", { name: "/v1/me" }).first()).toBeVisible();
    await settle(page, 300);
    await shot(page, "13-studio-status");
  });

  test("accesibilidad (axe) en panel, análisis y estado", async ({ page }) => {
    for (const url of ["/studio", "/studio/new", "/studio/status", "/studio/jobs"]) {
      await page.goto(url); await settle(page, 600);
      const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
      console.log(`axe ${url}:`, r.violations.map((v) => `${v.id}[${v.impact}](${v.nodes.length})`).join(", ") || "ninguna");
      expect(r.violations.filter((v) => v.impact === "critical" || v.impact === "serious"), url).toEqual([]);
    }
  });
});
