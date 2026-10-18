import type { Config } from "tailwindcss";

// Paleta inspirada en el lienzo oscuro de ManimCE (BLUE/TEAL/GREEN/YELLOW/RED), pero con contraste AA.
const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: { DEFAULT: "#0A0D14", 2: "#10141E", 3: "#171C28", line: "#242B3B" },
        ink: { DEFAULT: "#E8ECF4", dim: "#A3ADC2", faint: "#8A95AC" },
        mb: { blue: "#58C4DD", teal: "#5CD0B3", green: "#83C167", yellow: "#F4D35E", red: "#FC6255", violet: "#B189C6" },
      },
      fontFamily: {
        display: ['"Fraunces Variable"', "Georgia", "serif"],
        sans: ['"Inter Variable"', "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
      boxShadow: { glow: "0 0 0 1px rgba(88,196,221,.25), 0 10px 60px -10px rgba(88,196,221,.25)" },
      keyframes: {
        draw: { to: { strokeDashoffset: "0" } },
        floaty: { "0%,100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-6px)" } },
        fadeUp: { from: { opacity: "0", transform: "translateY(12px)" }, to: { opacity: "1", transform: "none" } },
      },
      animation: { floaty: "floaty 6s ease-in-out infinite", fadeUp: "fadeUp .6s ease-out both" },
    },
  },
  plugins: [],
};
export default config;
