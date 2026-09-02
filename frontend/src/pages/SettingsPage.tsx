import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function SettingsPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="API Endpoint" value="localhost" sub=":8000/api" delta="ONLINE" deltaColor="success" />
        <MetricCard label="Embedding Model" value="MiniLM-L6" sub="384-d" delta="LOADED" deltaColor="cyan" />
        <MetricCard label="Synthetic Mode" value="ON" sub="No real data" delta="LOCKED" deltaColor="violet" />
        <MetricCard label="Audit Log" value="Enabled" sub="All actions" delta="OK" deltaColor="warning" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-ink-100">Correlation Weights</h2>
            <RiskBadge label="CONFIG" level="LOW" />
          </div>
          <div className="space-y-3">
            {[
              { l: 'Stylometry', v: 0.22 },
              { l: 'PGP Fingerprint', v: 0.18 },
              { l: 'Wallet Prefix', v: 0.14 },
              { l: 'Behavioral', v: 0.12 },
              { l: 'Infrastructure', v: 0.10 },
              { l: 'Alias Overlap', v: 0.10 },
              { l: 'Time Pattern', v: 0.08 },
              { l: 'Topic Overlap', v: 0.06 },
            ].map(s => (
              <div key={s.l} className="flex items-center gap-3">
                <div className="text-xs text-muted-fg w-40">{s.l}</div>
                <div className="flex-1 h-1.5 rounded-full overflow-hidden" style={{ background: '#181c27' }}>
                  <div className="h-full rounded-full bg-cyan/80" style={{ width: `${s.v * 100}%`, background: '#06b6d4' }} />
                </div>
                <div className="text-xs font-mono text-ink-200 w-12 text-right">{s.v.toFixed(2)}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <h2 className="text-base font-semibold text-ink-100 mb-4">System</h2>
          <div className="space-y-2 text-sm">
            {[
              { k: 'Build', v: 'shadowlink-ai 0.1.0' },
              { k: 'Theme', v: 'Dark Intelligence' },
              { k: 'Animations', v: 'Framer Motion (enabled)' },
              { k: 'Data Source', v: 'Synthetic JSON (locked)' },
            ].map(r => (
              <div key={r.k} className="flex items-center justify-between py-2 border-t border-[#1f2433]">
                <div className="text-muted-fg">{r.k}</div>
                <div className="font-mono text-ink-100">{r.v}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
