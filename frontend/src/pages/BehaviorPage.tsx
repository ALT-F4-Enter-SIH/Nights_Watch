import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function BehaviorPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Active Sessions" value="14" sub="Tracked identities" delta="+3" deltaColor="cyan" />
        <MetricCard label="Night Ops" value="62%" sub="Activity 22:00–04:00" delta="HIGH" deltaColor="warning" />
        <MetricCard label="Burst Events" value="9" sub="Last 24h" delta="+4" deltaColor="critical" />
        <MetricCard label="Anomalies" value="3" sub="Unsupervised outliers" delta="NEW" deltaColor="violet" />
      </div>

      <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-ink-100">Behavioral Patterns</h2>
          <RiskBadge label="TIME-WINDOW" level="HIGH" />
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: 'Posting Cadence', v: 88, c: '#06b6d4' },
            { label: 'Time-of-Day Bias', v: 74, c: '#8b5cf6' },
            { label: 'Topic Drift', v: 41, c: '#f59e0b' },
            { label: 'Session Length', v: 67, c: '#10b981' },
          ].map(s => (
            <div key={s.label} className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
              <div className="text-[11px] text-muted-fg mb-1">{s.label}</div>
              <div className="text-2xl font-mono text-ink-100">{s.v}%</div>
              <div className="h-1.5 rounded-full overflow-hidden mt-2" style={{ background: '#181c27' }}>
                <div className="h-full rounded-full" style={{ width: `${s.v}%`, background: s.c }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
