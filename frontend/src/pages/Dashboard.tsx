import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import AnimatedNumber from '../components/analytics/AnimatedNumber'
import TimelineChart from '../components/analytics/TimelineChart'
import ConfidenceChart from '../components/analytics/ConfidenceChart'
import NetworkMiniGraph from '../components/analytics/NetworkMiniGraph'
import RiskBandChart from '../components/analytics/RiskBandChart'

/* Types matching backend DashboardResponse */
interface Overview {
  total_identities: number
  total_relations: number
  total_investigations: number
  avg_confidence: number
  high_confidence_count: number
  medium_confidence_count: number
  low_confidence_count: number
  open_investigations: number
  avg_risk_score: number
}
interface DashboardData {
  overview: Overview
  confidence_distribution: { bins: number[]; counts: number[]; label: string }
  category_breakdown: { category: string; count: number }[]
  risk_bands: { band: string; count: number }[]
  network_metrics: { total_nodes: number; total_edges: number; density: number; avg_clustering_coefficient: number; connected_components: number; isolated_nodes: number }
  recent_trends: { date: string; identities: number; relations: number }[]
}

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function load() {
      try {
        const res = await fetch('/api/dashboard')
        if (!res.ok) throw new Error(`${res.status}`)
        const json = await res.json()
        setData(json)
      } catch (e) {
        setError((e as Error).message)
        // Fallback synthetic data for premium demo continuity
        setData({
          overview: { total_identities: 47, total_relations: 112, total_investigations: 8, avg_confidence: 0.78, high_confidence_count: 34, medium_confidence_count: 41, low_confidence_count: 37, open_investigations: 5, avg_risk_score: 0.42 },
          confidence_distribution: { bins: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90], counts: [2, 4, 6, 8, 10, 14, 18, 24, 12, 10], label: 'Relations' },
          category_breakdown: [
            { category: 'Alias Overlap', count: 15 },
            { category: 'PGP Match', count: 12 },
            { category: 'Wallet Prefix', count: 8 },
            { category: 'Behavior', count: 7 },
            { category: 'Infrastructure', count: 5 },
          ],
          risk_bands: [
            { band: 'low', count: 18 },
            { band: 'medium', count: 16 },
            { band: 'high', count: 9 },
            { band: 'critical', count: 4 },
          ],
          network_metrics: { total_nodes: 47, total_edges: 112, density: 0.084, avg_clustering_coefficient: 0.231, connected_components: 5, isolated_nodes: 3 },
          recent_trends: [
            { date: '2026-08-27', identities: 42, relations: 98 },
            { date: '2026-08-28', identities: 43, relations: 100 },
            { date: '2026-08-29', identities: 44, relations: 103 },
            { date: '2026-08-30', identities: 45, relations: 106 },
            { date: '2026-08-31', identities: 46, relations: 109 },
            { date: '2026-09-01', identities: 47, relations: 111 },
            { date: '2026-09-02', identities: 47, relations: 112 },
          ],
        })
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="h-28 rounded-xl animate-pulse" style={{ background: '#0f1218', border: '1px solid #1f2433' }} />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 h-72 rounded-xl animate-pulse" style={{ background: '#0f1218', border: '1px solid #1f2433' }} />
          <div className="h-72 rounded-xl animate-pulse" style={{ background: '#0f1218', border: '1px solid #1f2433' }} />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-48 rounded-xl animate-pulse" style={{ background: '#0f1218', border: '1px solid #1f2433' }} />
          <div className="h-48 rounded-xl animate-pulse" style={{ background: '#0f1218', border: '1px solid #1f2433' }} />
        </div>
      </div>
    )
  }

  if (!data) {
    return <div className="text-sm text-muted-fg">Dashboard data unavailable.</div>
  }

  const { overview, confidence_distribution, risk_bands, network_metrics, recent_trends, category_breakdown } = data

  return (
    <motion.div
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-2xl font-bold tracking-tight text-ink-100">Intelligence Command Center</h2>
        <div className="text-[10px] font-mono text-muted-dim">Phase 9 · Real-time · {new Date().toISOString().slice(0, 10)}</div>
      </div>

      {/* Top Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="text-[11px] font-mono tracking-wider text-muted-dim uppercase mb-1">Active Investigations</div>
          <div className="text-3xl font-bold text-ink-100 tracking-tight">
            <AnimatedNumber value={overview.open_investigations} />
          </div>
          <div className="text-xs text-muted-fg mt-1">Open · <span className="text-cyan font-mono">{overview.total_investigations}</span> total</div>
        </div>
        <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="text-[11px] font-mono tracking-wider text-muted-dim uppercase mb-1">High Risk Entities</div>
          <div className="text-3xl font-bold text-ink-100 tracking-tight">
            <AnimatedNumber value={risk_bands.find(b => b.band === 'critical')?.count || 0} />
          </div>
          <div className="text-xs text-muted-fg mt-1">Critical band · <span className="text-violet font-mono">{network_metrics.total_nodes}</span> mapped</div>
        </div>
        <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="text-[11px] font-mono tracking-wider text-muted-dim uppercase mb-1">New Correlations</div>
          <div className="text-3xl font-bold text-ink-100 tracking-tight">
            <AnimatedNumber value={overview.high_confidence_count} />
          </div>
          <div className="text-xs text-muted-fg mt-1">Confidence ≥ 0.85 · <span className="text-success font-mono">{(overview.avg_confidence * 100).toFixed(0)}%</span> avg</div>
        </div>
        <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="text-[11px] font-mono tracking-wider text-muted-dim uppercase mb-1">AI Confidence</div>
          <div className="text-3xl font-bold tracking-tight">
            <span className={overview.avg_confidence >= 0.75 ? 'text-cyan' : overview.avg_confidence >= 0.55 ? 'text-violet' : 'text-warning'}>
              {(overview.avg_confidence * 100).toFixed(1)}%
            </span>
          </div>
          <div className="text-xs text-muted-fg mt-1">Across <span className="text-cyan font-mono">{overview.total_relations}</span> relations</div>
        </div>
      </div>

      {/* Section 1: Activity Timeline + Network */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TimelineChart data={recent_trends} />
        </div>
        <div>
          <NetworkMiniGraph nodes={network_metrics.total_nodes} edges={network_metrics.total_edges} />
        </div>
      </div>

      {/* Section 2: Correlation Confidence + Risk Bands */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ConfidenceChart bins={confidence_distribution.bins} counts={confidence_distribution.counts} label={confidence_distribution.label} />
        <RiskBandChart bands={risk_bands} />
      </div>

      {/* Section 3: Recent Correlations (feed) */}
      <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <h3 className="text-sm font-semibold text-ink-100 mb-4">Recent AI Correlations</h3>
        <div className="space-y-2">
          {[
            { pair: 'NightTrader · DarkPhoenix', score: 0.92, signal: 'PGP + Stylometry', status: 'Critical' },
            { pair: 'MarketEye · TradeSense', score: 0.78, signal: 'Behavioral + Wallet', status: 'High' },
            { pair: 'CyberWatch · NetHunter', score: 0.65, signal: 'Infrastructure', status: 'Medium' },
          ].map((c, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1, duration: 0.3 }}
              className="flex items-center gap-4 p-3 rounded-lg hover:bg-[#13131a] transition-colors"
              style={{ border: '1px solid #1f2433' }}
            >
              <div className="w-1.5 h-10 rounded-full bg-cyan/50 shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-ink-100">{c.pair}</div>
                <div className="text-[11px] text-muted-fg">{c.signal}</div>
              </div>
              <div className="text-right">
                <div className="text-sm font-mono text-cyan">{(c.score * 100).toFixed(0)}%</div>
                <div className={`text-[10px] font-mono ${c.status === 'Critical' ? 'text-critical' : c.status === 'High' ? 'text-warning' : 'text-violet'}`}>{c.status}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Section 4: High-Risk Entities + Category Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <h3 className="text-sm font-semibold text-ink-100 mb-4">High-Risk Entities</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { name: 'NightTrader', risk: 0.94, category: 'Alias Overlap' },
              { name: 'DarkPhoenix', risk: 0.91, category: 'PGP Match' },
              { name: 'MarketEye', risk: 0.73, category: 'Behavior' },
              { name: 'CyberWatch', risk: 0.61, category: 'Infrastructure' },
            ].map(e => (
              <div key={e.name} className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
                <div className="text-sm font-medium text-ink-100">{e.name}</div>
                <div className="text-[11px] text-muted-fg">{e.category}</div>
                <div className="mt-2 h-1.5 rounded-full bg-[#181c27] overflow-hidden">
                  <div className="h-full rounded-full bg-cyan/80" style={{ width: `${e.risk * 100}%` }} />
                </div>
                <div className="text-[11px] font-mono text-cyan mt-1">{(e.risk * 100).toFixed(0)}% risk</div>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <h3 className="text-sm font-semibold text-ink-100 mb-4">Category Breakdown</h3>
          <div className="space-y-3">
            {category_breakdown.map((cat) => (
              <div key={cat.category} className="flex items-center justify-between">
                <span className="text-xs text-muted-fg">{cat.category}</span>
                <span className="text-xs font-mono text-ink-200">{cat.count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Section 5: Investigation Status */}
      <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <h3 className="text-sm font-semibold text-ink-100 mb-4">Investigation Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
            <div className="text-2xl font-mono font-bold text-cyan">{overview.open_investigations}</div>
            <div className="text-xs text-muted-fg">Open · Active analysis</div>
          </div>
          <div className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
            <div className="text-2xl font-mono font-bold text-violet">{overview.total_investigations - overview.open_investigations}</div>
            <div className="text-xs text-muted-fg">Closed · Resolved</div>
          </div>
          <div className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
            <div className="text-2xl font-mono font-bold text-success">{overview.high_confidence_count}</div>
            <div className="text-xs text-muted-fg">High Confidence · Confirmed</div>
          </div>
        </div>
      </div>

      {/* Section 6: Bottom stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-xl p-4 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
          <div className="text-[11px] font-mono text-muted-dim">Graph Density</div>
          <div className="text-xl font-mono text-cyan">{network_metrics.density.toFixed(3)}</div>
        </div>
        <div className="rounded-xl p-4 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
          <div className="text-[11px] font-mono text-muted-dim">Clusters</div>
          <div className="text-xl font-mono text-violet">{network_metrics.connected_components}</div>
        </div>
        <div className="rounded-xl p-4 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
          <div className="text-[11px] font-mono text-muted-dim">Isolated Nodes</div>
          <div className="text-xl font-mono text-warning">{network_metrics.isolated_nodes}</div>
        </div>
        <div className="rounded-xl p-4 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
          <div className="text-[11px] font-mono text-muted-dim">Avg Clustering</div>
          <div className="text-xl font-mono text-success">{network_metrics.avg_clustering_coefficient.toFixed(2)}</div>
        </div>
      </div>

      {/* Footer note */}
      <div className="text-[10px] text-muted-dim font-mono">{error ? `Note: backend unreachable (${error}). Showing synthetic preview dataset.` : 'Data sourced from backend /api/dashboard · Synthetic / defensive-use only.'}</div>
    </motion.div>
  )
}
