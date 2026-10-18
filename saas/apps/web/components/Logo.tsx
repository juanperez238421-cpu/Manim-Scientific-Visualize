export function Logo({ className = "" }: { className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2.5 ${className}`}>
      <svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true">
        <rect x="1" y="1" width="30" height="30" rx="8" fill="#10141E" stroke="#242B3B" />
        <path d="M7 24 L7 8 M7 24 L25 24" stroke="#6F7A92" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M7 21 C 12 21, 14 10, 25 9" stroke="#58C4DD" strokeWidth="2.4" strokeLinecap="round" fill="none" />
        <circle cx="25" cy="9" r="2.3" fill="#F4D35E" />
      </svg>
      <span className="font-display text-lg font-semibold tracking-tight">AniMotion<span className="text-mb-blue">PDF</span></span>
    </span>
  );
}
