import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function InfrastructurePage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Hosts Mapped" value="23" sub="Synthetic infra" delta="+2" deltaColor="cyan" />
        <MetricCard label="ASN Clusters" value="4" sub="Network groups" delta="Stable" deltaColor="success" />
        <MetricCard label="Tor Exit Nodes" value="7" sub="Last 7 days" delta="+3" deltaColor="warning" />
        <MetricCard label="VPN Relays" value="11" sub="Detected tunnels" delta="+1" deltaColor="violet" />
      </div>

      <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-base font-semibold text-ink-100">Host Inventory</h2>
          <RiskBadge label="MOCK DATA" level="LOW" />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-[10px] uppercase tracking-wider text-muted-dim">
                <th className="py-2 px-2">Host</th>
                <th className="py-2 px-2">ASN</th>
                <th className="py-2 px-2">Country</th>
                <th className="py-2 px-2">Type</th>
                <th className="py-2 px-2 text-right">Risk</th>
              </tr>
            </thead>
            <tbody>
              {[
                { h: '185.220.101.42', a: 'AS9009', c: 'CH', t: 'Tor', r: 0.91 },
                { h: '45.33.32.156', a: 'AS63949', c: 'US', t: 'VPS', r: 0.42 },
                { h: '198.51.100.7', a: 'AS13335', c: 'DE', t: 'VPN', r: 0.78 },
                { h: '203.0.113.18', a: 'AS16509', c: 'NL', t: 'Hosting', r: 0.55 },
              ].map((row, i) => (
                <tr key={i} className="border-t border-[#1f2433]">
                  <td className="py-3 px-2 font-mono text-ink-100">{row.h}</td>
                  <td className="py-3 px-2 font-mono text-muted-fg">{row.a}</td>
                  <td className="py-3 px-2 text-muted-fg">{row.c}</td>
                  <td className="py-3 px-2 text-muted-fg">{row.t}</td>
                  <td className="py-3 px-2 text-right">
                    <span className="font-mono text-xs" style={{ color: row.r > 0.75 ? '#f43f5e' : row.r > 0.5 ? '#f59e0b' : '#10b981' }}>
                      {row.r.toFixed(2)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  )
}
