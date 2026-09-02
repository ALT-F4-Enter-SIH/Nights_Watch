import { motion } from 'framer-motion'

const COLORS: Record<string, string> = {
  critical: '#f43f5e',
  high: '#f59e0b',
  medium: '#06b6d4',
  low: '#10b981',
}

export default function RiskBandChart({ bands }: { bands: { band: string; count: number }[] }) {
  const max = Math.max(...bands.map(b => b.count), 1)
  return (
    <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
      <h3 className="text-sm font-semibold text-ink-100 mb-4">Risk Distribution</h3>
      <div className="space-y-3">
        {bands.map((b, i) => (
          <div key={b.band}>
            <div className="flex justify-between text-[11px] mb-1">
              <span className="text-muted-fg uppercase font-mono tracking-wider">{b.band}</span>
              <span className="font-mono text-ink-200">{b.count}</span>
            </div>
            <div className="h-2 rounded-full overflow-hidden" style={{ background: '#181c27' }}>
              <motion.div
                className="h-full rounded-full"
                style={{ background: COLORS[b.band] }}
                initial={{ width: 0 }}
                animate={{ width: `${(b.count / max) * 100}%` }}
                transition={{ delay: 0.1 + i * 0.08, duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
