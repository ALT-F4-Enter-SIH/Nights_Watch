import { motion } from 'framer-motion'

export default function ConfidenceChart({ bins, counts, label = 'Relations' }: { bins: number[]; counts: number[]; label?: string }) {
  const max = Math.max(...counts, 1)
  const w = 360, h = 160
  const barWidth = w / bins.length - 4
  return (
    <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-ink-100">Correlation Confidence</h3>
        <span className="text-[10px] font-mono text-muted-fg uppercase tracking-wider">{label}</span>
      </div>
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-auto">
        {/* baseline */}
        <line x1={0} y1={h - 14} x2={w} y2={h - 14} stroke="#1f2433" strokeWidth={1} />
        {bins.map((b, i) => {
          const h2 = (counts[i] / max) * (h - 30)
          const x = i * (w / bins.length) + 2
          const y = h - 14 - h2
          const isHigh = b >= 70
          return (
            <g key={b}>
              <motion.rect
                x={x} width={barWidth} y={h - 14} height={0}
                animate={{ y, height: h2 }} transition={{ delay: i * 0.04, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                fill={isHigh ? '#06b6d4' : '#1f2937'}
                rx={2}
              />
              <text x={x + barWidth / 2} y={h - 4} textAnchor="middle" fontSize={8} fill="#6b7280" fontFamily="monospace">{b}</text>
              {counts[i] > 0 && (
                <text x={x + barWidth / 2} y={y - 4} textAnchor="middle" fontSize={9} fill="#94a3b8" fontFamily="monospace">{counts[i]}</text>
              )}
            </g>
          )
        })}
      </svg>
      <div className="flex justify-between text-[10px] text-muted-fg font-mono mt-1">
        <span>Low · 0%</span>
        <span>High · 100%</span>
      </div>
    </div>
  )
}
