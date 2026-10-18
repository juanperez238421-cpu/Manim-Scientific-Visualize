import { clerk } from "@clerk/testing/playwright";
import { expect, test } from "@playwright/test";
import path from "node:path";
import { EVIDENCE } from "./helpers";

test("móvil: dashboard y lista de trabajos sin desbordamiento horizontal", async ({ page }) => {
  test.skip(!process.env.E2E_CLERK_USER_EMAIL, "BLOCKED: define E2E_CLERK_USER_EMAIL");
  await page.goto("/");
  await clerk.signIn({ page, emailAddress: process.env.E2E_CLERK_USER_EMAIL! });
  for (const route of ["/app", "/app/create", "/app/jobs", "/app/credits"]) {
    await page.goto(route);
    await page.waitForLoadState("networkidle");
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, `desbordamiento horizontal en ${route}`).toBeLessThanOrEqual(1);
    await page.screenshot({ path: path.join(EVIDENCE, `ui_mobile_${route.replace(/\W+/g, "_")}.png`), fullPage: true });
  }
});
