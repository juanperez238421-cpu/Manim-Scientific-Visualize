"use client";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, onCall, ApiError, type Balance, type CallRecord, type RenderOptions, type User } from "@/lib/api";

type Health = "checking" | "up" | "down";
interface Ctx {
  me: User | null; balance: Balance | null; options: RenderOptions | null; health: Health; error: ApiError | null;
  calls: CallRecord[]; refresh: () => Promise<void>; loading: boolean;
}
const C = createContext<Ctx | null>(null);
export const useStudio = () => { const v = useContext(C); if (!v) throw new Error("StudioProvider ausente"); return v; };

export function StudioProvider({ children }: { children: React.ReactNode }) {
  const [me, setMe] = useState<User | null>(null);
  const [balance, setBalance] = useState<Balance | null>(null);
  const [options, setOptions] = useState<RenderOptions | null>(null);
  const [health, setHealth] = useState<Health>("checking");
  const [error, setError] = useState<ApiError | null>(null);
  const [calls, setCalls] = useState<CallRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => onCall((r) => setCalls((p) => [r, ...p].slice(0, 60))), []);

  const refresh = useCallback(async () => {
    setLoading(true); setError(null);
    try { await api.health(); setHealth("up"); } catch { setHealth("down"); setLoading(false); setError(new ApiError(0, "network_error", "No se pudo conectar con la API.")); return; }
    try {
      const [m, b, o] = await Promise.all([api.me(), api.balance(), api.renderOptions()]);
      setMe(m); setBalance(b); setOptions(o);
    } catch (e) { setError(e instanceof ApiError ? e : new ApiError(0, "unknown", String(e))); }
    setLoading(false);
  }, []);
  useEffect(() => { void refresh(); }, [refresh]);

  const v = useMemo(() => ({ me, balance, options, health, error, calls, refresh, loading }), [me, balance, options, health, error, calls, refresh, loading]);
  return <C.Provider value={v}>{children}</C.Provider>;
}
