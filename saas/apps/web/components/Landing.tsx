import Link from "next/link";
import { Logo } from "./Logo";
import { HeroDemo } from "./HeroDemo";
import { StatusBadge } from "./StatusBadge";

const NAV = [["Cómo funciona", "#como-funciona"], ["Ejemplos", "#ejemplos"], ["Planes", "#planes"], ["Preguntas", "#faq"]] as const;

export function Nav() {
  return (
    <header className="sticky top-0 z-40 border-b border-canvas-line/70 bg-canvas/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3 sm:px-6">
        <Link href="/" className="focus-ring rounded-lg" aria-label="AniMotionPDF, inicio"><Logo /></Link>
        <nav aria-label="Principal" className="hidden items-center gap-7 text-sm text-ink-dim md:flex">
          {NAV.map(([l, h]) => (<a key={h} href={h} className="focus-ring rounded hover:text-ink">{l}</a>))}
        </nav>
        <div className="flex items-center gap-2">
          <Link href="/studio" className="btn-ghost hidden sm:inline-flex">Iniciar sesión</Link>
          <Link href="/studio" className="btn-primary">Abrir Studio</Link>
        </div>
      </div>
      <nav aria-label="Secciones" className="flex gap-5 overflow-x-auto border-t border-canvas-line/60 px-4 py-2 text-xs text-ink-dim md:hidden">
        {NAV.map(([l, h]) => (<a key={h} href={h} className="focus-ring whitespace-nowrap rounded py-1 hover:text-ink">{l}</a>))}
      </nav>
    </header>
  );
}

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="bg-axes absolute inset-0" aria-hidden="true" />
      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-4 pb-20 pt-14 sm:px-6 lg:grid-cols-[1.05fr_1fr] lg:pt-24">
        <div className="animate-fadeUp">
          <span className="chip border-mb-yellow/40 bg-mb-yellow/10 text-mb-yellow">Versión preliminar · en desarrollo</span>
          <h1 className="h-display mt-5 text-4xl font-semibold leading-[1.08] sm:text-5xl lg:text-[3.4rem]">
            Tu hoja de ejercicios, <span className="text-mb-blue">resuelta paso a paso</span> en animación científica.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-ink-dim">
            Sube un PDF de matemáticas o física, elige los ejercicios y obtén un video animado con ManimCE. Cada solución se contrasta con cálculo numérico independiente cuando es posible — y te decimos con claridad cuándo no lo es.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/studio/new" className="btn-primary">Probar con un PDF</Link>
            <a href="#como-funciona" className="btn-ghost">Ver cómo funciona</a>
          </div>
          <dl className="mt-10 grid max-w-lg grid-cols-3 gap-4 text-sm">
            {[["Preanálisis", "antes de gastar créditos"], ["Verificación", "numérica y trazable"], ["Cotización", "transparente y previa"]].map(([t, d]) => (
              <div key={t} className="border-l-2 border-mb-blue/50 pl-3"><dt className="font-semibold">{t}</dt><dd className="text-xs text-ink-faint">{d}</dd></div>
            ))}
          </dl>
        </div>
        <HeroDemo />
      </div>
    </section>
  );
}

const STEPS = [
  { n: "01", t: "Sube tu PDF", d: "Validamos tipo, tamaño, huella SHA-256, páginas y si hay capa de texto u OCR. Sin sorpresas después.", c: "text-mb-blue" },
  { n: "02", t: "Preanálisis", d: "Detectamos ejercicios, temas y dificultad académica y visual. Si algo es incierto, lo marcamos en lugar de adivinar.", c: "text-mb-teal" },
  { n: "03", t: "Elige y cotiza", d: "Selecciona ejercicios, configura el video y revisa el desglose de créditos antes de autorizar nada.", c: "text-mb-yellow" },
  { n: "04", t: "Video verificado", d: "Un worker renderiza con ManimCE, comprobamos el MP4 y te mostramos el estado de verificación real.", c: "text-mb-green" },
];
export function How() {
  return (
    <section id="como-funciona" className="mx-auto max-w-6xl scroll-mt-28 px-4 py-20 sm:px-6">
      <h2 className="h-display text-3xl font-semibold sm:text-4xl">De PDF a video, sin cajas negras</h2>
      <p className="mt-3 max-w-2xl text-ink-dim">Cuatro pasos, cada uno con su propio estado visible. Lo que aún no existe aparece como «pendiente» o «no disponible», nunca simulado.</p>
      <ol className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {STEPS.map((s) => (
          <li key={s.n} className="card p-5">
            <span className={`font-mono text-sm ${s.c}`}>{s.n}</span>
            <h3 className="mt-3 font-display text-xl font-semibold">{s.t}</h3>
            <p className="mt-2 text-sm leading-relaxed text-ink-dim">{s.d}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}

export function Gallery() {
  const placeholders = ["Cinemática: caída libre", "Cálculo: regla de la cadena"];
  return (
    <section id="ejemplos" className="mx-auto max-w-6xl scroll-mt-28 px-4 py-20 sm:px-6">
      <h2 className="h-display text-3xl font-semibold sm:text-4xl">Ejemplos</h2>
      <p className="mt-3 max-w-2xl text-ink-dim">Todavía no hay videos generados desde un PDF por esta plataforma. Aquí distinguimos con rigor lo real de lo pendiente.</p>
      <div className="mt-10 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        <figure className="card overflow-hidden md:col-span-2">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/gallery/Centerofmass1.gif" alt="Animación ManimCE de un centro de masa con puntos y vectores sobre fondo oscuro" className="aspect-video w-full border-b border-canvas-line bg-white object-contain" />
          <figcaption className="space-y-2 p-4">
            <StatusBadge status="real" label="Render real de ManimCE" />
            <p className="text-sm text-ink-dim">Animación de la biblioteca del proyecto. <strong className="text-ink">No fue generada desde un PDF</strong> por el pipeline de AniMotionPDF; muestra el estilo visual del motor.</p>
          </figcaption>
        </figure>
        {placeholders.map((p) => (
          <figure key={p} className="card flex flex-col overflow-hidden">
            <div className="flex aspect-video items-center justify-center border-b border-canvas-line bg-canvas bg-[radial-gradient(circle_at_30%_30%,rgba(88,196,221,.08),transparent_60%)]">
              <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#6F7A92" strokeWidth="1.5" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5" /><path d="M10 9.5l5 2.5-5 2.5z" /></svg>
            </div>
            <figcaption className="space-y-2 p-4"><StatusBadge status="pending" label="Marcador de posición" /><p className="text-sm text-ink-dim">{p}</p></figcaption>
          </figure>
        ))}
      </div>
    </section>
  );
}

const PLANS = [
  { n: "Free", p: "0,00", cr: 30, pdf: "5 págs.", sec: "60 s", res: "720p", pro: false },
  { n: "Starter", p: "19,00", cr: 300, pdf: "20 págs.", sec: "480 s", res: "1080p", pro: true },
  { n: "Pro", p: "59,00", cr: 1200, pdf: "60 págs.", sec: "900 s", res: "1080p", pro: true },
];
export function Plans() {
  return (
    <section id="planes" className="mx-auto max-w-6xl scroll-mt-28 px-4 py-20 sm:px-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <h2 className="h-display text-3xl font-semibold sm:text-4xl">Planes y créditos</h2>
        <span className="chip border-mb-red/40 bg-mb-red/10 text-mb-red">Precios provisionales · sin aprobar · sin cobros</span>
      </div>
      <p className="mt-3 max-w-2xl text-ink-dim">Valores borrador del backend (<code className="font-mono text-xs">draft-0.1</code>); la moneda y las tarifas se fijarán tras medir costos reales. Hoy no hay pasarela de pago activa.</p>
      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {PLANS.map((p) => (
          <article key={p.n} className="card p-6">
            <h3 className="font-display text-2xl font-semibold">{p.n}</h3>
            <p className="mt-2 text-3xl font-semibold">{p.p}<span className="ml-1 text-sm font-normal text-ink-faint">/mes (borrador)</span></p>
            <ul className="mt-5 space-y-2 text-sm text-ink-dim">
              <li><strong className="text-ink">{p.cr}</strong> créditos al mes</li><li>PDF de hasta {p.pdf}</li><li>Video de hasta {p.sec}</li><li>Resolución máxima {p.res}</li>
              <li>{p.pro ? "Prólogo three.js permitido" : "Sin prólogo three.js"}</li>
            </ul>
          </article>
        ))}
      </div>
      <p className="mt-4 text-xs text-ink-faint">Fuente: <code className="font-mono">saas/db/seed_plans_DRAFT.sql</code>. Los pesos por segundo (SVG 0,5 · Manim 1,0 · three.js 2,5) también son borrador.</p>
    </section>
  );
}

const FAQ = [
  ["¿Los videos ya se generan?", "Aún no desde esta interfaz. El motor de render (M2) y el análisis (M3) se desarrollan por separado; esta versión muestra el flujo real de carga y cotización y marca como pendiente lo demás."],
  ["¿Cómo sé si la solución es correcta?", "Cuando el problema es determinista, se recalcula con herramientas numéricas independientes. Si solo se compara con la respuesta impresa en el documento, lo indicamos: eso no es verificación independiente."],
  ["¿Me cobran al subir un PDF?", "No. Subir y analizar no consume créditos. Los créditos se reservan solo cuando autorizas un trabajo con un máximo explícito, y hoy no hay cobros reales."],
  ["¿Qué PDFs funcionan mejor?", "Hojas con texto seleccionable, en español o inglés. Los escaneos requieren OCR, que se marca como riesgo; el manuscrito o investigación avanzada puede quedar «en revisión»."],
  ["¿Mis documentos son privados?", "Se almacenan en un bucket privado con URLs firmadas de corta duración y acceso restringido a tu cuenta."],
] as const;
export function Faq() {
  return (
    <section id="faq" className="mx-auto max-w-3xl scroll-mt-28 px-4 py-20 sm:px-6">
      <h2 className="h-display text-3xl font-semibold sm:text-4xl">Preguntas frecuentes</h2>
      <div className="mt-8 divide-y divide-canvas-line rounded-2xl border border-canvas-line bg-canvas-2/60">
        {FAQ.map(([q, a]) => (
          <details key={q} className="group px-5 py-4">
            <summary className="focus-ring flex cursor-pointer items-center justify-between gap-4 rounded font-medium">{q}<span aria-hidden="true" className="text-mb-blue transition group-open:rotate-45">+</span></summary>
            <p className="mt-3 text-sm leading-relaxed text-ink-dim">{a}</p>
          </details>
        ))}
      </div>
    </section>
  );
}

export function Cta() {
  return (
    <section className="mx-auto max-w-6xl px-4 pb-24 sm:px-6">
      <div className="card relative overflow-hidden p-8 text-center sm:p-14">
        <div className="bg-axes absolute inset-0 opacity-60" aria-hidden="true" />
        <div className="relative">
          <h2 className="h-display text-3xl font-semibold sm:text-4xl">Empieza con un preanálisis gratuito</h2>
          <p className="mx-auto mt-3 max-w-xl text-ink-dim">Sube un PDF y mira qué ejercicios detectamos, su dificultad y una cotización no vinculante. Sin cobros.</p>
          <Link href="/studio/new" className="btn-primary mt-7">Abrir Studio</Link>
        </div>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-canvas-line py-8 text-center text-xs text-ink-faint">
      <Logo className="mb-3 justify-center" />
      <p>AniMotionPDF · versión preliminar M4 · precios y capacidades provisionales.</p>
      <p className="mt-1"><Link href="/studio/status" className="focus-ring rounded underline hover:text-ink">Estado de capacidades</Link></p>
    </footer>
  );
}
