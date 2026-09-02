import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function EvidencePage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Evidence Items" value="86" sub="Synthetic artifacts" delta="+8" deltaColor="cyan" />
        <MetricCard label="Custody Chain" value="100%" sub="Integrity verified" delta="OK" deltaColor="success" />
        <MetricCard label="Pending Review" value="5" sub="Awaiting analyst" delta="+2" deltaColor="warning" />
        <MetricCard label="Sealed" value="12" sub="Locked records" delta="Stable" deltaColor="violet" />
      </div>

      <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-ink-100">Recent Evidence</h2>
          <RiskBadge label="CHAIN-OF-CUSTODY" level="MEDIUM" />
        </div>
        <div className="space-y-3">
          {[
            { id: 'EV-2026-0142', kind: 'Forum post', source: 'NightTrader', hash: 'a3f9…c0d1', status: 'Sealed' },
            { id: 'EV-2026-0141', kind: 'PGP key', source: 'DarkPhoenix', hash: '7b21…ee09', status: 'Verified' },
            { id: 'EV-2026-0140', kind: 'Wallet addr', source: 'MarketEye', hash: '0x9c…aa11', status: 'Pending' },
          ].map((e, i) => (
            <div key={i} className="flex items-center gap-3 p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
              <div className="w-1.5 h-10 rounded-full bg-violet/40 shrink-0" />
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-ink-100">{e.kind} · {e.source}</div>
                <div className="text-[11px] text-muted-fg font-mono mt-0.5">{e.id} · sha256 {e.hash}</div>
              </div>
              <div className="text-xs font-mono text-muted-fg">{e.status}</div>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  )
}
