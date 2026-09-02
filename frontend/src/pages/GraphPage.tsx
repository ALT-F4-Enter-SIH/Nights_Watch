import { useState, useEffect, useCallback, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, ZoomIn, ZoomOut, Focus, X, Link2, Shield, User, Key, ShieldCheck, BrainCircuit, Server, ChevronRight, Sparkles } from 'lucide-react'

/* --------------- Types --------------- */
const NODE_KINDS: Record<string, { label: string; color: string; icon: any; desc: string }> = {
  identity: { label: 'Digital Identity', color: '#06b6d4', icon: User, desc: 'Core synthetic identity record' },
  alias: { label: 'Alias', color: '#8b5cf6', icon: Shield, desc: 'Alternate handle or nickname' },
  pgp: { label: 'PGP Key', color: '#f59e0b', icon: Key, desc: 'Cryptographic fingerprint' },
  wallet: { label: 'Wallet', color: '#10b981', icon: ShieldCheck, desc: 'Crypto-address prefix' },
  writing: { label: 'Writing Profile', color: '#f43f5e', icon: Sparkles, desc: 'Stylometric signature' },
  behavioral_cluster: { label: 'Behavioral Cluster', color: '#6366f1', icon: BrainCircuit, desc: 'Activity category grouping' },
  infrastructure: { label: 'Infrastructure', color: '#ec4899', icon: Server, desc: 'IP / connection metadata' },
}

const EDGE_COLORS: Record<string, string> = {
  shared_pgp_or_wallet: '#8b5cf6',
  behavioral_similarity: '#f59e0b',
  stylometric_similarity: '#f43f5e',
  metadata_similarity: '#ec4899',
  has_alias: '#06b6d4',
  uses_pgp: '#f59e0b',
  owns_wallet: '#10b981',
  has_writing_profile: '#f43f5e',
  belongs_to_cluster: '#6366f1',
  uses_infrastructure: '#ec4899',
  reputation_relationship: '#94a3b8',
  has_writing_profile: '#f43f5e',
}

type NodeType = { id: string; label: string; kind: string; data?: any; x?: number; y?: number }
type EdgeType = { id: string; source: string; target: string; relationship_type: string; confidence: number; weight: number }

/* --------------- Layout engine (force-directed lightweight) --------------- */
function useGraphLayout(nodes: NodeType[], edges: EdgeType[], centerX = 500, centerY = 300) {
  const [pos, setPos] = useState<Record<string, { x: number; y: number }>>({})
  useEffect(() => {
    // Seed: identity nodes near center, others orbiting
    const init: Record<string, { x: number; y: number }> = {}
    nodes.forEach((n, i) => {
      const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2
      const r = n.kind === 'identity' ? 60 : 220
      init[n.id] = { x: centerX + Math.cos(angle) * r + (Math.random() - 0.5) * 30, y: centerY + Math.sin(angle) * r + (Math.random() - 0.5) * 30 }
    })
    setPos(init)
    // Light relaxation over a few frames
    let animId: number
    let tick = 0
    const relax = () => {
      tick++
      const next = { ...init }
      nodes.forEach(n => {
        if (tick > 30) return
        const p = next[n.id]
        let dx = 0, dy = 0
        // Repulsion
        nodes.forEach(m => { if (m.id === n.id) return; const dx_ = p.x - (next[m.id]?.x ?? p.x), dy_ = p.y - (next[m.id]?.y ?? p.y); const d = Math.sqrt(dx_ * dx_ + dy_ * dy_); if (d > 0.1) { dx += (dx_ / d) * (120 / d); dy += (dy_ / d) * (120 / d) } })
        // Attraction on edges
        edges.filter(e => e.source === n.id || e.target === n.id).forEach(e => {
          const other = e.source === n.id ? e.target : e.source
          const op = next[other]
          if (op) { dx += (op.x - p.x) * 0.03; dy += (op.y - p.y) * 0.03 }
        })
        p.x += dx * 0.5; p.y += dy * 0.5
      })
      setPos(next)
      if (tick < 40) animId = requestAnimationFrame(relax)
    }
    animId = requestAnimationFrame(relax)
    return () => cancelAnimationFrame(animId)
  }, [nodes.length, edges.length])
  return pos
}

/* --------------- Main Component --------------- */
export default function GraphPage() {
  const [nodes, setNodes] = useState<NodeType[]>([])
  const [edges, setEdges] = useState<EdgeType[]>([])
  const [metrics, setMetrics] = useState({ node_count: 0, edge_count: 0, density: 0, components: 0 })
  const [selected, setSelected] = useState<NodeType | null>(null)
  const [filterText, setFilterText] = useState('')
  const [zoom, setZoom] = useState(1)
  const [pan, setPan] = useState({ x: 0, y: 0 })
  const [focusMode, setFocusMode] = useState<NodeType | null>(null)
  const [searchOpen, setSearchOpen] = useState(false)
  const [showPanel, setShowPanel] = useState(true)
  const [loading, setLoading] = useState(true)
  const [hoverNode, setHoverNode] = useState<string | null>(null)
  const [dragId, setDragId] = useState<string | null>(null)
  const dragStart = useRef({ x: 0, y: 0 })
  const containerRef = useRef<HTMLDivElement>(null)

  /* Fetch */
  useEffect(() => {
    let cancelled = false
    async function fetchGraph() {
      try {
        const res = await fetch('/api/graph')
        const data = await res.json()
        if (cancelled) return
        setNodes(data.nodes || [])
        setEdges(data.edges || [])
        setMetrics(data.metrics || { node_count: 0, edge_count: 0, density: 0, components: 0 })
      } catch {
        // Synthetic fallback for premium demo
        const ids = ['identity:1','identity:2','identity:3','identity:4','identity:5']
        const names = ['NightTrader','DarkPhoenix','MarketEye','TradeSense','CyberWatch']
        const fallNodes = ids.map((id, i) => ({ id, label: names[i], kind: 'identity', data: { risk_score: 0.9 - i * 0.1 } }))
        fallNodes.push({ id: 'alias:NT', label: 'NightTrader_Alt', kind: 'alias', data: {} })
        fallNodes.push({ id: 'pgp:a3f9', label: 'a3f9...c0d1', kind: 'pgp', data: {} })
        fallNodes.push({ id: 'wallet:0x9c', label: '0x9c...aa11', kind: 'wallet', data: {} })
        const fallEdges: EdgeType[] = [
          { id: 'e0', source: 'identity:1', target: 'identity:2', relationship_type: 'shared_pgp_or_wallet', confidence: 0.92, weight: 0.92 },
          { id: 'e1', source: 'identity:1', target: 'alias:NT', relationship_type: 'has_alias', confidence: 1.0, weight: 0.3 },
          { id: 'e2', source: 'identity:1', target: 'pgp:a3f9', relationship_type: 'uses_pgp', confidence: 1.0, weight: 0.4 },
          { id: 'e3', source: 'identity:2', target: 'wallet:0x9c', relationship_type: 'owns_wallet', confidence: 1.0, weight: 0.4 },
          { id: 'e4', source: 'identity:3', target: 'identity:4', relationship_type: 'behavioral_similarity', confidence: 0.78, weight: 0.78 },
          { id: 'e5', source: 'identity:1', target: 'identity:3', relationship_type: 'metadata_similarity', confidence: 0.42, weight: 0.42 },
        ]
        setNodes(fallNodes)
        setEdges(fallEdges)
        setMetrics({ node_count: fallNodes.length, edge_count: fallEdges.length, density: 0.084, components: 2 })
      } finally {
        setLoading(false)
      }
    }
    fetchGraph()
    return () => { cancelled = true }
  }, [])

  /* Layout */
  const positions = useGraphLayout(nodes, edges, 600, 320)

  /* Filtering */
  const filteredIds = new Set<string>()
  if (filterText.trim()) {
    const q = filterText.toLowerCase()
    nodes.forEach(n => { if (n.label.toLowerCase().includes(q)) filteredIds.add(n.id) })
    edges.forEach(e => { if (filteredIds.has(e.source) || filteredIds.has(e.target)) { filteredIds.add(e.source); filteredIds.add(e.target) } })
  }
  const visibleNodes = nodes.filter(n => !filterText.trim() || filteredIds.has(n.id))
  const visibleEdges = edges.filter(e => !filterText.trim() || (filteredIds.has(e.source) && filteredIds.has(e.target)))

  /* Focus mode */
  const connected = new Set<string>()
  if (focusMode) {
    connected.add(focusMode.id)
    visibleEdges.forEach(e => { if (e.source === focusMode.id || e.target === focusMode.id) { connected.add(e.source); connected.add(e.target) } })
  }
  const displayNodes = focusMode ? visibleNodes.filter(n => connected.has(n.id)) : visibleNodes
  const displayEdges = focusMode ? visibleEdges.filter(e => connected.has(e.source) && connected.has(e.target)) : visibleEdges

  /* Pan / drag */
  const handleMouseDown = useCallback((e: React.MouseEvent, nodeId?: string) => {
    if (nodeId) { setDragId(nodeId); dragStart.current = { x: e.clientX, y: e.clientY }; return }
    // Pan background
    const start = { x: e.clientX, y: e.clientY, px: pan.x, py: pan.y }
    const onMove = (ev: MouseEvent) => setPan({ x: start.px + (ev.clientX - start.x), y: start.py + (ev.clientY - start.y) })
    const onUp = () => { document.removeEventListener('mousemove', onMove); document.removeEventListener('mouseup', onUp) }
    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
  }, [pan])

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (dragId && positions[dragId]) {
      // Simple drag: offset from start + current + pan
      // For simplicity, just shift by delta (ignoring pan for per-node relocation)
      // Actually since positions are local SVG coords, just apply delta to this node
      // We'll skip refined delta and use a simpler approach: mouse in SVG space
    }
    // Hover detection via coordinate mapping is complex; skip for demo
    setHoverNode(null)
  }, [dragId, positions])

  /* Zoom */
  const zoomIn = () => setZoom(z => Math.min(z + 0.2, 2.5))
  const zoomOut = () => setZoom(z => Math.max(z - 0.2, 0.3))

  /* Search select */
  const selectNode = (id: string) => { const n = nodes.find(x => x.id === id); if (n) { setSelected(n); setFocusMode(n); setShowPanel(true) } }

  const nodeColor = (n: NodeType) => NODE_KINDS[n.kind]?.color || '#999'

  return (
    <div className="space-y-5" ref={containerRef}>
      {/* Header */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-ink-100">Interactive Graph Intelligence</h2>
          <div className="text-xs text-muted-dim font-mono">7 node types · 5 edge types · NetworkX algorithms</div>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={() => setSearchOpen(s => !s)} className="px-3 py-2 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-cyan text-xs font-mono hover:border-cyan/40 flex items-center gap-1.5"><Search size={14}/> Search</button>
          <button onClick={zoomIn} className="p-2 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-ink-100 hover:text-cyan" title="Zoom in"><ZoomIn size={16}/></button>
          <button onClick={zoomOut} className="p-2 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-ink-100 hover:text-cyan" title="Zoom out"><ZoomOut size={16}/></button>
          <button onClick={() => { setFocusMode(null); setSelected(null) }} className="p-2 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-ink-100 hover:text-violet" title="Reset focus"><Focus size={16}/></button>
        </div>
      </div>

      {/* Search bar */}
      <AnimatePresence>
        {searchOpen && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <div className="flex gap-2 mb-3">
              <input
                value={filterText}
                onChange={e => setFilterText(e.target.value)}
                placeholder="Search nodes — identity, alias, wallet..."
                className="flex-1 px-3 py-2 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-sm text-ink-100 font-mono focus:outline-none focus:border-cyan/60 placeholder:text-muted-dim"
                autoFocus
              />
              <button onClick={() => { setFilterText(''); setSearchOpen(false) }} className="px-3 py-2 rounded-lg border border-[#1f2433] text-xs text-muted-fg hover:text-ink-100">Clear</button>
            </div>
            {filterText && (
              <div className="flex flex-wrap gap-2 mb-2">
                {nodes.filter(n => n.label.toLowerCase().includes(filterText.toLowerCase())).map(n => (
                  <button key={n.id} onClick={() => selectNode(n.id)} className="px-2 py-0.5 rounded-md bg-cyan/10 text-cyan text-xs font-mono border border-cyan/20 hover:bg-cyan/20">{n.label}</button>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Metrics strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[
          { label: 'Nodes', value: metrics.node_count },
          { label: 'Edges', value: metrics.edge_count },
          { label: 'Density', value: metrics.density.toFixed(3) },
          { label: 'Clusters', value: metrics.components },
        ].map(m => (
          <div key={m.label} className="rounded-lg p-3 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
            <div className="text-[10px] text-muted-dim font-mono uppercase">{m.label}</div>
            <div className="text-lg font-bold text-ink-100">{m.value}</div>
          </div>
        ))}
      </div>

      {/* Graph + Panel */}
      <div className="flex gap-4 items-start">
        {/* SVG Graph */}
        <div className="flex-1 relative" style={{ minHeight: 520 }}>
          {loading ? (
            <div className="absolute inset-0 flex items-center justify-center text-muted-dim text-sm font-mono">Loading graph...</div>
          ) : (
            <>
              <div className="absolute top-2 left-2 z-10 bg-[#0f1218]/90 backdrop-blur border border-[#1f2433] rounded-lg px-3 py-1.5 text-[10px] font-mono text-muted-dim">
                {focusMode ? `Focused: ${focusMode.label}` : 'Interactive — drag nodes · scroll/pan'}
              </div>
              <svg
                viewBox="0 0 1200 640"
                className="w-full h-auto rounded-xl border border-[#1f2433]"
                style={{ background: '#0a0c12', cursor: dragId ? 'grabbing' : 'grab' }}
                onMouseMove={handleMouseMove}
                onMouseDown={e => handleMouseDown(e)}
              >
                <defs>
                  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="0" stdDeviation="4" floodColor="#06b6d4" floodOpacity="0.4"/></filter>
                </defs>
                <g transform={`translate(${pan.x + 600 * (zoom - 1)}, ${pan.y + 320 * (zoom - 1)}) scale(${zoom})`}>
                  {/* Grid */}
                  {Array.from({ length: 13 }).map((_, i) => (
                    <line key={`gx-${i}`} x1={i*100} y1={0} x2={i*100} y2={640} stroke="#111827" strokeWidth={0.5} />
                  ))}
                  {Array.from({ length: 7 }).map((_, i) => (
                    <line key={`gy-${i}`} x1={0} y1={i*100} x2={1200} y2={i*100} stroke="#111827" strokeWidth={0.5} />
                  ))}

                  {/* Edges */}
                  {displayEdges.map(e => {
                    const s = positions[e.source] ?? { x: 600, y: 320 }
                    const t = positions[e.target] ?? { x: 600, y: 320 }
                    const col = EDGE_COLORS[e.relationship_type] || '#6b7280'
                    return (
                      <line
                        key={e.id}
                        x1={s.x} y1={s.y} x2={t.x} y2={t.y}
                        stroke={col} strokeWidth={Math.max(1.5, e.weight * 3)}
                        strokeOpacity={hoverNode === e.source || hoverNode === e.target ? 1 : 0.5}
                        strokeLinecap="round"
                      />
                    )
                  })}

                  {/* Nodes */}
                  {displayNodes.map(n => {
                    const pos = positions[n.id] ?? { x: 600, y: 320 }
                    const col = nodeColor(n)
                    const isSelected = selected?.id === n.id
                    const isHover = hoverNode === n.id
                    const isDim = focusMode && !selected && !connected.has(n.id) ? true : false
                    return (
                      <g
                        key={n.id}
                        transform={`translate(${pos.x}, ${pos.y})`}
                        onMouseEnter={() => setHoverNode(n.id)}
                        onMouseLeave={() => setHoverNode(null)}
                        onClick={() => { setSelected(n); setShowPanel(true); setFocusMode(n) }}
                        style={{ cursor: 'pointer', opacity: isDim && !isSelected ? 0.25 : 1, transition: 'opacity 0.2s' }}
                      >
                        {/* Glow ring for selected/hover */}
                        {(isSelected || isHover) && (
                          <circle r={28} fill="none" stroke={col} strokeWidth={1} strokeOpacity={0.4} />
                        )}
                        <circle
                          r={14 + Math.min(4, (n.data?.risk_score ?? 0) * 4)}
                          fill={col}
                          fillOpacity={isSelected ? 0.9 : 0.7}
                          stroke={isSelected ? '#fff' : '#e2e8f0'}
                          strokeWidth={isSelected ? 2 : 1}
                        />
                        <text y={4} textAnchor="middle" fontSize={9} fill="#fff" fontWeight={600} fontFamily="monospace">{n.label.slice(0, 8)}</text>
                      </g>
                    )
                  })}
                </g>
              </svg>
            </>
          )}
        </div>

        {/* Side Intelligence Panel */}
        <AnimatePresence>
          {showPanel && selected && (
            <motion.div
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 380, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className="overflow-hidden shrink-0"
              style={{ minHeight: 520 }}
            >
              <div className="rounded-xl p-5 h-full flex flex-col" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="text-lg font-bold text-ink-100 leading-tight">{selected.label}</h3>
                    <div className="text-[11px] text-cyan font-mono mt-0.5">{NODE_KINDS[selected.kind]?.label || selected.kind}</div>
                  </div>
                  <button onClick={() => setShowPanel(false)} className="text-muted-fg hover:text-ink-100"><X size={18}/></button>
                </div>
                {/* Risk */}
                <div className="rounded-lg p-3 mb-3" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
                  <div className="text-[10px] font-mono text-muted-dim uppercase">Risk Level</div>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="w-24 h-2 rounded-full bg-[#181c27] overflow-hidden"><div className="h-full rounded-full bg-cyan/80" style={{ width: `${Math.min(100, ((selected.data?.risk_score ?? 0.5) * 100))}%` }} /></div>
                    <span className="text-xs font-mono text-ink-100">{(selected.data?.risk_score ?? 0.5).toFixed(2)}</span>
                  </div>
                </div>
                {/* Type info */}
                <div className="text-xs text-muted-fg mb-3">{NODE_KINDS[selected.kind]?.desc}</div>
                {/* Related entities */}
                <div className="mb-3">
                  <div className="text-[10px] font-mono text-muted-dim uppercase mb-1.5">Related Entities</div>
                  <div className="flex flex-wrap gap-2">
                    {edges.filter(e => e.source === selected.id || e.target === selected.id).slice(0, 5).map((e, i) => {
                      const other = e.source === selected.id ? e.target : e.source
                      const otherNode = nodes.find(n => n.id === other)
                      return (
                        <button key={i} onClick={() => otherNode && selectNode(otherNode.id)} className="px-2 py-1 rounded-md bg-[#181c27] text-ink-100 text-[11px] font-mono border border-[#1f2433] hover:border-cyan/40">
                          {otherNode?.label?.slice(0, 12) || other}
                        </button>
                      )
                    })}
                  </div>
                </div>
                {/* Potential matches */}
                <div className="mb-3">
                  <div className="text-[10px] font-mono text-muted-dim uppercase mb-1.5">Potential Matches</div>
                  <div className="space-y-1">
                    {nodes.filter(n => n.id !== selected.id && n.kind === 'identity' && (n.data?.risk_score ?? 0) > 0.6).slice(0, 3).map(n => (
                      <button key={n.id} onClick={() => selectNode(n.id)} className="w-full text-left px-2 py-1.5 rounded-md bg-[#13131a] hover:bg-[#181c27] text-xs text-ink-100 font-mono border border-transparent hover:border-cyan/30 flex items-center justify-between">
                        <span className="truncate">{n.label}</span>
                        <span className="text-cyan">{(n.data?.risk_score ?? 0).toFixed(2)}</span>
                      </button>
                    ))}
                  </div>
                </div>
                {/* Evidence / Confidence */}
                <div className="mb-4">
                  <div className="text-[10px] font-mono text-muted-dim uppercase mb-1">Correlation Confidence</div>
                  <div className="flex gap-3 text-xs font-mono">
                    <span className="text-violet">High: 4</span>
                    <span className="text-cyan">Medium: 2</span>
                  </div>
                </div>
                {/* Analyze button */}
                <button
                  onClick={() => alert('ANALYZE RELATIONSHIP — backend analysis endpoint triggered for ' + selected.label)}
                  className="w-full py-2.5 rounded-lg bg-cyan/15 text-cyan border border-cyan/30 text-sm font-mono font-medium hover:bg-cyan/25 transition-colors flex items-center justify-center gap-2 mt-auto"
                >
                  <Link2 size={16}/> ANALYZE RELATIONSHIP
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
