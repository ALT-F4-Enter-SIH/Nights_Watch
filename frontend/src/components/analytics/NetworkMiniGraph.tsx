export default function NetworkMiniGraph({ nodes, edges }: { nodes: number; edges: number }) {
  const cx = 180, cy = 100, r = 70
  const nodeCount = Math.min(nodes, 12)
  const points = Array.from({ length: nodeCount }, (_, i) => {
    const a = (i / nodeCount) * Math.PI * 2 - Math.PI / 2
    return { x: cx + Math.cos(a) * r * 0.8, y: cy + Math.sin(a) * r * 0.8 }
  })
  return (
    <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-ink-100">Network Intelligence</h3>
        <span className="text-[10px] font-mono text-cyan">{edges} edges · {nodes} nodes</span>
      </div>
      <svg viewBox="0 0 360 200" className="w-full h-auto">
        {/* edges */}
        {points.map((p, i) => (
          <line
            key={`e-${i}`}
            x1={p.x} y1={p.y}
            x2={points[(i + 2) % nodeCount].x} y2={points[(i + 2) % nodeCount].y}
            stroke="#2a3547" strokeWidth={1}
          />
        ))}
        {/* nodes */}
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r={6} fill="#06b6d4" opacity={0.9} />
            <circle cx={p.x} cy={p.y} r={10} fill="#06b6d4" fillOpacity={0.1} />
          </g>
        ))}
      </svg>
      <div className="flex gap-4 mt-2 text-[11px] font-mono text-muted-fg">
        <span><span className="text-cyan font-bold">{nodes}</span> entities</span>
        <span><span className="text-violet font-bold">{Math.round(edges / Math.max(nodes, 1) * 10) / 10}</span> density</span>
      </div>
    </div>
  )
}
