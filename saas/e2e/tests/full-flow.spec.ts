import { clerk } from "@clerk/testing/playwright";
import { expect, test } from "@playwright/test";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { EVIDENCE, ROOT, devDb } from "./helpers";

const PDF = process.env.E2E_PDF || path.join(ROOT, "engine/pdf2video/examples/physics/physics_worksheet.pdf");
const RESOLUTION = process.env.E2E_RESOLUTION || "720p";
const JOB_TIMEOUT = Number(process.env.E2E_JOB_TIMEOUT_MS || 45 * 60_000);
const EMAIL = process.env.E2E_CLERK_USER_EMAIL;

test("PDF -> job -> MP4 verificado -> reproducción y descarga (Clerk Development, API real, worker real)", async ({ page }, info) => {
  test.skip(!EMAIL, "BLOCKED: define E2E_CLERK_USER_EMAIL (usuario creado en Clerk Development, p. ej. e2e+clerk_test@example.com)");
  expect(fs.existsSync(PDF), `no existe el PDF de prueba ${PDF}`).toBeTruthy();

  // 1) autenticación real con Clerk (sign-in token de la API de backend de Clerk; sin contraseña en el repo)
  await page.goto("/");
  await clerk.signIn({ page, emailAddress: EMAIL! });
  await page.goto("/app");
  await expect(page).toHaveURL(/\/app/);
  const sub = await page.evaluate(() => (window as any).Clerk?.user?.id as string);
  expect(sub, "no se obtuvo el id de usuario de Clerk").toMatch(/^user_/);

  // 2) créditos y plan de DESARROLLO para el usuario de prueba (BD local)
  await page.reload();                                   // fuerza /v1/me => crea la fila del usuario en PostgreSQL
  devDb("--grant-credits", sub, "5000");
  devDb("--set-plan", sub, "starter");

  // 3) asistente: subir PDF (URL firmada directa), configurar, autorizar créditos
  await page.goto("/app/create");
  await page.getByLabel("Seleccionar PDF").setInputFiles(PDF);
  await page.getByRole("button", { name: /Subir y verificar PDF/ }).click();
  await expect(page.getByText(/PDF verificado/)).toBeVisible({ timeout: 60_000 });
  await page.getByLabel("Resolución").selectOption(RESOLUTION);
  await page.getByRole("button", { name: /Estimar créditos/ }).click();
  await expect(page.getByText(/MÁXIMO A AUTORIZAR/)).toBeVisible();
  await page.getByLabel(/Autorizo reservar/).check();
  await page.screenshot({ path: path.join(EVIDENCE, "ui_01_autorizacion.png"), fullPage: true });
  await page.getByRole("button", { name: /Confirmar e iniciar/ }).click();
  await page.waitForURL(/\/app\/jobs\/[0-9a-f-]{36}/);
  const jobId = page.url().split("/").pop()!;
  info.annotations.push({ type: "job_id", description: jobId });

  // 4) progreso y estado final (la página refresca cada 5 s)
  await expect(page.getByText(/Video disponible/)).toBeVisible({ timeout: JOB_TIMEOUT });
  await page.screenshot({ path: path.join(EVIDENCE, "ui_02_job_completado.png"), fullPage: true });
  await expect(page.getByTestId("verification-status")).toContainText(/Verificada/);
  await expect(page.getByTestId("verification-status")).not.toContainText(/parcialmente|revisión/);

  // 5) reproducción real en el navegador
  await page.getByRole("button", { name: /Reproducir/ }).click();
  const video = page.locator("video.studio-video");
  await expect(video).toBeVisible();
  await expect.poll(() => video.evaluate((v: HTMLVideoElement) => v.readyState), { timeout: 60_000 }).toBeGreaterThanOrEqual(2);
  const meta = await video.evaluate((v: HTMLVideoElement) => ({ w: v.videoWidth, h: v.videoHeight, d: v.duration }));
  expect(meta.h).toBe(Number(RESOLUTION.replace("p", "")));
  expect(meta.d).toBeGreaterThan(5);
  await video.evaluate(async (v: HTMLVideoElement) => { v.muted = true; await v.play(); });
  await page.waitForTimeout(3000);
  const t1 = await video.evaluate((v: HTMLVideoElement) => v.currentTime);
  expect(t1, "el video no avanza").toBeGreaterThan(1);
  await video.evaluate((v: HTMLVideoElement) => { v.currentTime = Math.max(1, v.duration - 3); });   // seek (usa Range 206)
  await page.waitForTimeout(1500);
  expect(await video.evaluate((v: HTMLVideoElement) => v.error)).toBeNull();
  await page.screenshot({ path: path.join(EVIDENCE, "ui_03_reproduccion.png"), fullPage: true });

  // 6) descarga y comparación con lo que el navegador reproduce
  const [dl] = await Promise.all([page.waitForEvent("download"), page.getByRole("button", { name: /Descargar/ }).click()]);
  const out = path.join(EVIDENCE, `descarga_${jobId}.mp4`);
  await dl.saveAs(out);
  const buf = fs.readFileSync(out);
  expect(buf.length).toBeGreaterThan(10_000);
  expect(buf.subarray(4, 8).toString()).toBe("ftyp");
  fs.writeFileSync(path.join(EVIDENCE, `descarga_${jobId}.sha256`), `${crypto.createHash("sha256").update(buf).digest("hex")}  ${path.basename(out)}\n`);
  info.annotations.push({ type: "download", description: `${buf.length} bytes` });
});
