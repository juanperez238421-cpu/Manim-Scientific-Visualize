import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { settle, shot } from "./helpers";

test.describe("Landing", () => {
  test("desktop: contenido, honestidad de estados y captura", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto("/");
    await settle(page);
    await expect(page.getByRole("heading", { level: 1 })).toContainText("resuelta paso a paso");
    for (const h of ["De PDF a video, sin cajas negras", "Ejemplos", "Planes y créditos", "Preguntas frecuentes"]) await expect(page.getByRole("heading", { name: h })).toBeVisible();
    await expect(page.getByText("no es un video generado").first()).toBeVisible();
    await expect(page.getByText("Render real de ManimCE")).toBeVisible();
    await expect(page.getByText("Marcador de posición")).toHaveCount(2);
    await expect(page.getByText("Precios provisionales · sin aprobar · sin cobros")).toBeVisible();
    await shot(page, "01-landing-desktop-hero", false);
    await shot(page, "02-landing-desktop-full");
  });
  test("FAQ es operable con teclado", async ({ page }) => {
    await page.goto("/");
    const q = page.getByText("¿Los videos ya se generan?");
    await q.focus(); await page.keyboard.press("Enter");
    await expect(page.getByText("Aún no desde esta interfaz")).toBeVisible();
  });
  test("navegación: Abrir Studio lleva al panel", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("link", { name: "Abrir Studio" }).first().click();
    await expect(page).toHaveURL(/\/studio$/);
  });
  test("móvil 390px: sin desbordamiento horizontal", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/"); await settle(page);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow).toBeLessThanOrEqual(0);
    await shot(page, "03-landing-mobile-hero", false);
    await shot(page, "04-landing-mobile-full");
  });
  test("accesibilidad (axe, WCAG A/AA)", async ({ page }) => {
    await page.goto("/"); await settle(page, 500);
    const r = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa"]).analyze();
    console.log("axe landing violations:", r.violations.map((v) => `${v.id}(${v.nodes.length})`).join(", ") || "ninguna");
    expect(r.violations.filter((v) => v.impact === "critical" || v.impact === "serious")).toEqual([]);
  });
});
