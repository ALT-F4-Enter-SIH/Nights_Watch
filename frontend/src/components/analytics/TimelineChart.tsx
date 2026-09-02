import { motion } from 'framer-motion'

export default function TimelineChart({ data }: { data: { date: string; identities: number; relations: number }[] }) {
  const maxId = Math.max(...data.map(d => d.identities), 1)
  const maxRel = Math.max(...data.map(d => d.relations), 1)
  const w = 720, h = 160, margin = { top: 10, right: 10, bottom: 30, left: 36 }
  const innerW = w - margin.left - margin.right
  const innerH = h - margin.top - margin.bottom
  const xStep = innerW / (data.length - 1 || 1)
  const yScale = (v: number, max: number) => innerH - (v / max) * innerH

  return (
    <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
      <h3 className="text-sm font-semibold text-ink-100 mb-4">Threat Activity Timeline — 7 Days</h3>
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-auto" preserveAspectRatio="none">
        {/* grid */}
        {[0, 0.25, 0.5, 0.75, 1].map(t => (
          <line key={t} x1={margin.left} y1={margin.top + t * innerH} x2={w - margin.right} y2={margin.top + t * innerH} stroke="#181c27" strokeWidth={1} />
        ))}
        {/* lines */}
        <polyline
          fill="none" stroke="#06b6d4" strokeWidth={2.5}
          points={data.map((d, i) => {
            const x = margin.left + i * xStep
            const y = margin.top + yScale(d.identities, maxId)
            return `${x},${y}`
          }).join(' ')}
        />
        <polyline
          fill="none" stroke="#8b5cf6" strokeWidth={2.5}
          points={data.map((d, i) => {
            const x = margin.left + i * xStep
            const y = margin.top + yScale(d.relations, maxRel)
            return `${x},${y}`
          }).join(' ')}
        />
        {/* dots */}
        {data.map((d, i) => {
          const x = margin.left + i * xStep
          const yId = margin.top + yScale(d.identities, maxId)
          const yRel = margin.top + yScale(d.relations, maxRel)
          return (
            <g key={i}>
              <circle cx={x} cy={yId} r={3.5} fill="#06b6d4" />
              <circle cx={x} cy={yRel} r={3.5} fill="#8b5cf6" />
              <text x={x} y={h - 4} textAnchor="middle" fontSize={9} fill="#6b7280" fontFamily="monospace">{d.date.slice(5)}</text>
            </g>
          )
        })}
      </svg>
      <div className="flex gap-6 mt-2 text-[11px] font-mono text-muted-fg">
        <span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-cyan" /> Identities</span>
        <span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-violet" /> Relations</span>
      </div>
    </div>
  )
}
