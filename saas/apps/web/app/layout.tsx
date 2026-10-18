import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "AniMotionPDF — Videos científicos desde tus PDFs", template: "%s · AniMotionPDF" },
  description: "Sube un PDF de matemáticas o física, elige ejercicios y obtén soluciones animadas con ManimCE. Versión preliminar en desarrollo.",
};
export const viewport: Viewport = { themeColor: "#0A0D14", width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50 focus:rounded-lg focus:bg-mb-blue focus:px-4 focus:py-2 focus:text-canvas">Saltar al contenido</a>
        {children}
      </body>
    </html>
  );
}
