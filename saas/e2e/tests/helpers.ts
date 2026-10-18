import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import dotenv from "dotenv";

export const ROOT = path.resolve(__dirname, "../..");
export const EVIDENCE = path.join(ROOT, "storage", "evidence");
fs.mkdirSync(EVIDENCE, { recursive: true });

const env = dotenv.parse(fs.readFileSync(path.join(ROOT, ".env")));
const PY = path.join(ROOT, ".venv", process.platform === "win32" ? "Scripts/python.exe" : "bin/python");

/** Operaciones de DESARROLLO sobre la BD local (créditos/plan de prueba). Nunca se usan contra una BD remota. */
export function devDb(...args: string[]) {
  if (!/@(127\.0\.0\.1|localhost)[:/]/.test(env.DATABASE_URL || "")) throw new Error("DATABASE_URL no es local: se rechaza por seguridad");
  return execFileSync(PY, [path.join(ROOT, "saas/apps/api/scripts/migrate.py"), ...args], { env: { ...process.env, DATABASE_URL: env.DATABASE_URL }, encoding: "utf-8" });
}
