import { NextRequest, NextResponse } from "next/server";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, writeFile, readFile, rm, mkdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { promisify } from "node:util";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";
const run = promisify(execFile);
const MAX_BYTES = 10 * 1024 * 1024;
const SCRIPT = process.env.SDI_PREFLIGHT_SCRIPT ?? "";
const CACHE_DIR = path.join(process.cwd(), ".cache", "preflight");

/**
 * ADAPTADOR DE DESARROLLO hacia el analizador SDI real (M3). El backend FastAPI aún no expone
 * GET /v1/uploads/{id}/analysis (M3-D no implementado), así que este endpoint ejecuta el analizador local.
 * - Desactivado salvo M4_LOCAL_PREFLIGHT=1 y SDI_PREFLIGHT_SCRIPT definido.
 * - El PDF es dato no confiable: sin shell, `python -I`, tiempo y tamaño acotados, nombre de archivo fijo.
 * - Sin llamadas a Anthropic ni renders: el analizador es determinista y local.
 */
export async function POST(req: NextRequest) {
  if (process.env.M4_LOCAL_PREFLIGHT !== "1" || !SCRIPT)
    return NextResponse.json({ code: "preflight_unavailable", message: "Análisis local no habilitado en este entorno." }, { status: 501 });

  const form = await req.formData().catch(() => null);
  const file = form?.get("file");
  const select = String(form?.get("select") ?? "");
  if (!(file instanceof File)) return NextResponse.json({ code: "bad_request", message: "Falta el archivo." }, { status: 400 });
  if (select && !/^ex\d{3}(,ex\d{3}){0,29}$/.test(select)) return NextResponse.json({ code: "bad_request", message: "Selección inválida." }, { status: 400 });
  if (file.size > MAX_BYTES) return NextResponse.json({ code: "too_large", message: "PDF mayor a 10 MB." }, { status: 413 });
  const bytes = Buffer.from(await file.arrayBuffer());
  if (bytes.subarray(0, 5).toString("latin1") !== "%PDF-") return NextResponse.json({ code: "invalid_pdf", message: "No es un PDF válido." }, { status: 422 });

  const sha = createHash("sha256").update(bytes).digest("hex");
  const key = path.join(CACHE_DIR, `${sha}.${select ? select.replace(/,/g, "_") : "all"}.json`);
  try {
    const hit = await readFile(key, "utf8");
    return NextResponse.json({ report: JSON.parse(hit), sha256: sha, elapsed_ms: 0, cached: true, source: "local_sdi_analyzer" });
  } catch { /* sin caché */ }

  const dir = await mkdtemp(path.join(tmpdir(), "m4-sdi-"));
  const t0 = Date.now();
  try {
    await writeFile(path.join(dir, "input.pdf"), bytes);
    const args = ["-I", SCRIPT, path.join(dir, "input.pdf"), "--plan", "starter", "--out", dir];
    if (select) args.push("--select", select);
    await run(process.env.PYTHON_BIN ?? "python3", args, { timeout: 60_000, maxBuffer: 5 * 1024 * 1024, cwd: dir });
    const report = JSON.parse(await readFile(path.join(dir, "input.preflight.json"), "utf8"));
    await mkdir(CACHE_DIR, { recursive: true });
    await writeFile(key, JSON.stringify(report));
    return NextResponse.json({ report, sha256: sha, elapsed_ms: Date.now() - t0, cached: false, source: "local_sdi_analyzer" });
  } catch (e) {
    return NextResponse.json({ code: "preflight_failed", message: "El analizador no pudo procesar el PDF." }, { status: 502 });
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}
