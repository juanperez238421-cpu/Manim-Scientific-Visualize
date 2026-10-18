/**
 * Ilustración de interfaz (NO es un video generado): muestra el flujo PDF → análisis → gráfica v–t con los datos
 * del ejercicio de ejemplo (v₀=10 m/s, v=30 m/s, t=5 s → a=4 m/s², cálculo determinista).
 */
export function HeroDemo() {
  return (
    <figure className="relative mx-auto w-full max-w-xl" aria-labelledby="hero-demo-cap">
      <div className="absolute -inset-6 -z-10 rounded-[2rem] bg-mb-blue/10 blur-3xl" aria-hidden="true" />
      <div className="card shadow-glow overflow-hidden">
        <div className="flex items-center gap-2 border-b border-canvas-line px-4 py-2.5 text-xs text-ink-faint">
          <span className="h-2.5 w-2.5 rounded-full bg-mb-red/70" /><span className="h-2.5 w-2.5 rounded-full bg-mb-yellow/70" /><span className="h-2.5 w-2.5 rounded-full bg-mb-green/70" />
          <span className="ml-2 font-mono">hoja_cinematica.pdf → ejercicio 1</span>
        </div>
        <div className="grid grid-cols-[0.9fr_1.4fr] gap-0">
          <div className="border-r border-canvas-line p-4">
            <div className="rounded-lg bg-white/95 p-3 text-[9px] leading-relaxed text-slate-700 shadow-inner" aria-hidden="true">
              <div className="mb-1.5 h-1.5 w-3/4 rounded bg-slate-400" />
              {[90, 100, 70, 95, 60, 85, 40].map((w, i) => (<div key={i} className="mb-1 h-1 rounded bg-slate-300" style={{ width: `${w}%` }} />))}
              <div className="mt-2 rounded border-2 border-mb-blue bg-mb-blue/10 p-1.5">
                <div className="mb-1 h-1 w-full rounded bg-slate-500" /><div className="h-1 w-2/3 rounded bg-slate-500" />
              </div>
              {[80, 55].map((w, i) => (<div key={i} className="mt-1 h-1 rounded bg-slate-300" style={{ width: `${w}%` }} />))}
            </div>
            <ul className="mt-3 space-y-1.5 text-[11px] text-ink-dim">
              <li className="pop" style={{ animationDelay: ".3s" }}><span className="text-mb-green">✓</span> Ejercicio detectado</li>
              <li className="pop" style={{ animationDelay: ".7s" }}><span className="text-mb-green">✓</span> Datos: v₀, v, t</li>
              <li className="pop" style={{ animationDelay: "1.1s" }}><span className="text-mb-yellow">◌</span> Verificación numérica</li>
            </ul>
          </div>
          <div className="bg-canvas p-3">
            <svg viewBox="0 0 440 320" role="img" aria-label="Gráfica velocidad contra tiempo con pendiente 4 metros por segundo al cuadrado" className="w-full">
              <defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#58C4DD" stopOpacity=".35" /><stop offset="1" stopColor="#58C4DD" stopOpacity="0" /></linearGradient></defs>
              {[0, 1, 2, 3, 4, 5, 6].map((i) => (<line key={`v${i}`} x1={50 + i * 60} y1="20" x2={50 + i * 60} y2="270" stroke="#242B3B" strokeWidth="1" />))}
              {[0, 1, 2, 3, 4, 5].map((i) => (<line key={`h${i}`} x1="50" y1={270 - i * 50} x2="410" y2={270 - i * 50} stroke="#242B3B" strokeWidth="1" />))}
              <path d="M50 270 L50 14 M50 270 L424 270" stroke="#A3ADC2" strokeWidth="1.6" fill="none" markerEnd="url(#none)" />
              <path d="M50 200 L350 60 L350 270 L50 270 Z" fill="url(#area)" className="pop" style={{ animationDelay: "2.2s" }} />
              <path d="M50 200 L350 60" stroke="#58C4DD" strokeWidth="3.5" strokeLinecap="round" fill="none" className="draw" style={{ ["--len" as string]: 332 }} />
              <path d="M350 60 L350 270" stroke="#F4D35E" strokeWidth="1.6" strokeDasharray="5 5" className="pop" style={{ animationDelay: "2.4s" }} />
              <circle cx="50" cy="200" r="5" fill="#FC6255" /><circle cx="350" cy="60" r="5.5" fill="#F4D35E" className="pop" style={{ animationDelay: "2.2s" }} />
              <text x="58" y="190" fill="#FC6255" fontSize="12" fontFamily="JetBrains Mono">v₀=10</text>
              <text x="300" y="48" fill="#F4D35E" fontSize="12" fontFamily="JetBrains Mono" className="pop" style={{ animationDelay: "2.2s" }}>v=30</text>
              <text x="338" y="290" fill="#A3ADC2" fontSize="12" fontFamily="JetBrains Mono">t=5 s</text>
              <text x="58" y="26" fill="#A3ADC2" fontSize="12" fontFamily="JetBrains Mono">v (m/s)</text>
              <text x="170" y="150" fill="#E8ECF4" fontSize="17" fontFamily="Fraunces Variable, serif" className="pop" style={{ animationDelay: "2.8s" }} transform="rotate(-20 170 150)">a = Δv/Δt = 4 m/s²</text>
            </svg>
          </div>
        </div>
      </div>
      <figcaption id="hero-demo-cap" className="mt-3 text-center text-xs text-ink-faint">
        Ilustración de la interfaz — <strong className="text-ink-dim">no es un video generado</strong>. Los valores son los de un ejercicio de cinemática de ejemplo.
      </figcaption>
    </figure>
  );
}
