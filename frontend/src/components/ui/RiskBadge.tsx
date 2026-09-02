interface Props {
  label: string
  level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
}

const COLORS = {
  LOW: { bg: 'rgba(10,184,151,0.08)', border: '#0a6b4a', text: '#10b981', glow: 'rgba(16,185,129,0.2)' },
  MEDIUM: { bg: 'rgba(245,158,11,0.08)', border: '#8a5c10', text: '#f59e0b', glow: 'rgba(245,158,11,0.2)' },
  HIGH: { bg: 'rgba(168,139,250,0.08)', border: '#5b3e9a', text: '#a78bfa', glow: 'rgba(168,139,250,0.2)' },
  CRITICAL: { bg: 'rgba(239,68,68,0.08)', border: '#8a2b2b', text: '#ef4444', glow: 'rgba(239,68,68,0.2)' },
}

export default function RiskBadge({ label, level }: Props) {
  const c = COLORS[level]
  return (
    <span
      className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-[11px] font-semibold tracking-wide2 border"
      style={{
        background: c.bg,
        borderColor: c.border,
        color: c.text,
        boxShadow: `0 0 0 1px ${c.glow}`,
      }}
    >
      <span className="w-1.5 h-1.5 rounded-full animate-pulseDot" style={{ background: c.text }} />
      {label}
    </span>
  )
}
