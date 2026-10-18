import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";
const IDP = process.env.DEV_IDP_URL ?? "http://127.0.0.1:9100";

/** Solo para desarrollo local: desactivada salvo DEV_AUTH=1. Nunca debe habilitarse en staging público. */
export async function GET(req: NextRequest) {
  if (process.env.DEV_AUTH !== "1") return NextResponse.json({ code: "dev_auth_disabled" }, { status: 404 });
  const sub = (req.nextUrl.searchParams.get("sub") ?? "user_m4_demo").replace(/[^a-zA-Z0-9_\-]/g, "").slice(0, 40) || "user_m4_demo";
  try {
    const r = await fetch(`${IDP}/token?sub=${sub}&email=${sub}@dev.test`, { cache: "no-store" });
    if (!r.ok) throw new Error(String(r.status));
    return NextResponse.json({ token: await r.text() });
  } catch {
    return NextResponse.json({ code: "idp_unreachable" }, { status: 502 });
  }
}
