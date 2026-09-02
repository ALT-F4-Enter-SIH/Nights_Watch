import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function ReportsPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Reports Generated" value="24" sub="Last 30 days" delta="+5" deltaColor="cyan" />
        <MetricCard label="Exports" value="PDF / JSON" sub="Authorized review" delta="READY" deltaColor="success" />
        <MetricCard label="Avg Build Time" value="3.2s" sub="Per report" delta="-0.4s" deltaColor="violet" />
        <MetricCard label="Methodology" value="Embedded" sub="Explainability on" delta="ON" deltaColor="warning" />
      </div>

      <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-ink-100">Available Templates</h2>
          <RiskBadge label="DEFENSIVE USE" level="LOW" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {[
            { t: 'Cluster Correlation', d: 'Multi-signal breakdown of an identity cluster.' },
            { t: 'Stylometry Compare', d: 'Pairwise writing-style analysis with weights.' },
            { t: 'Graph Snapshot', d: 'NetworkX sub-graph + centrality export.' },
          ].map((r, i) => (
            <div key={i} className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
              <div className="text-sm font-medium text-ink-100 mb-1">{r.t}</div>
              <div className="text-[11px] text-muted-fg">{r.d}</div>
              <button className="mt-3 text-[11px] font-mono text-cyan hover:underline">Generate →</button>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
