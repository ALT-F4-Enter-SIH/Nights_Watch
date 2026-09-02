import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'
import { ShieldCheck, Network, Sparkles, FileText, Clock, UserCheck, Layers, ChevronRight } from 'lucide-react'

const INV = {
  id: 'INV-2026-001',
  title: 'OPERATION SHADOW MARKET',
  status: 'ACTIVE',
  priority: 'HIGH',
  created: '2026-08-12',
  updated: '2026-09-02',
  entities: 24,
  links: 47,
  correlations: 18,
  analyst: 'Agent K',
}

const TABS = [
  { key: 'overview', label: 'Overview', icon: Layers },
  { key: 'entities', label: 'Entities', icon: UserCheck },
  { key: 'graph', label: 'Graph', icon: Network },
  { key: 'ai', label: 'AI Analysis', icon: Sparkles },
  { key: 'timeline', label: 'Timeline', icon: Clock },
  { key: 'evidence', label: 'Evidence', icon: ShieldCheck },
  { key: 'report', label: 'Report', icon: FileText },
]

export default function InvestigationsPage() {
  const [tab, setTab] = useState('overview')

  return (
    <div className="space-y-5">
      {/* Investigation header */}
      <div className="rounded-2xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)' }}>
        <div className="flex flex-wrap items-start gap-4 justify-between mb-4">
          <div>
            <div className="text-[10px] font-mono text-muted-dim uppercase tracking-widest mb-1">Investigation ID · {INV.id}</div>
            <h2 className="text-2xl font-extrabold text-ink-100 tracking-tight">{INV.title}</h2>
            <p className="text-xs text-muted-fg mt-1">Active synthetic analysis · Defensive research only</p>
          </div>
          <div className="flex gap-3 items-center">
            <RiskBadge label={INV.status} level={INV.priority === 'HIGH' ? 'HIGH' : 'MEDIUM'} />
            <div className="text-[10px] font-mono text-muted-dim">{INV.priority} priority</div>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <MetricCard label="Entities" value={String(INV.entities)} sub="Linked identities" delta="+4" deltaColor="cyan" />
          <MetricCard label="Potential Links" value={String(INV.links)} sub="Cross-reference hits" delta="+12" deltaColor="violet" />
          <MetricCard label="AI Correlations" value={String(INV.correlations)} sub="Confirmed by engine" delta="+6" deltaColor="success" />
          <MetricCard label="Status" value={INV.status} sub={`${INV.updated} · Analyst ${INV.analyst}`} delta="OPEN" deltaColor="warning" />
        </div>
      </div>

      {/* Tab bar */}
      <div className="flex gap-1 overflow-x-auto pb-1">
        {TABS.map(t => {
          const Icon = t.icon
          return (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-mono whitespace-nowrap transition-all ${tab === t.key ? 'bg-cyan/10 text-cyan border border-cyan/20' : 'text-muted-fg hover:text-ink-100 border border-transparent hover:border-[#1f2433]'}`}
            >
              <Icon size={14}/> {t.label}
            </button>
          )
        })}
      </div>

      {/* Tab content */}
      <AnimatePresence mode="wait">
        <motion.div key={tab} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -6 }} transition={{ duration: 0.2 }}>
          {tab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
                <h3 className="text-base font-semibold text-ink-100 mb-3">Investigation Scope</h3>
                <div className="text-sm text-muted-fg leading-relaxed mb-3">Operation Shadow Market examines a synthetic identity cluster suspected of coordinated activity across dark-market forums, crypto wallets, and alias networks. Analysis uses Phase 4 correlation engine + Phase 7 graph intelligence.</div>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { label: 'Synthetic Data', v: 'Only' },
                    { label: 'Methodology', v: '8-signal weighted' },
                    { label: 'Verification', v: 'Human required' },
                  ].map(s => (
                    <div key={s.label} className="rounded-lg p-3 text-center bg-[#13131a] border border-[#1f2433]">
                      <div className="text-[10px] text-muted-dim font-mono">{s.label}</div>
                      <div className="text-xs font-bold text-ink-100">{s.v}</div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
                <h3 className="text-base font-semibold text-ink-100 mb-3">Quick Actions</h3>
                <div className="space-y-2">
                  {[
                    'Select identities → Run AI Analysis',
                    'Explore graph relationships',
                    'Review evidence items',
                    'Generate final report',
                  ].map((a, i) => (
                    <button key={i} onClick={() => setTab(i === 0 ? 'entities' : i === 1 ? 'graph' : i === 2 ? 'evidence' : 'report')} className="w-full text-left px-3 py-2.5 rounded-lg bg-[#13131a] border border-[#1f2433] text-xs text-ink-100 font-mono hover:border-cyan/40 flex items-center justify-between group">
                      <span>{a}</span><ChevronRight size={12} className="text-muted-dim group-hover:text-cyan" />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
          {tab === 'entities' && (
            <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-3">Linked Entities ({INV.entities})</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {['NightTrader', 'DarkPhoenix', 'MarketEye', 'TradeSense', 'CyberWatch', 'NetHunter', 'ShadowLink', 'GhostLink', 'CryptoBot', 'VaultEye'].map(n => (
                  <button key={n} onClick={() => setTab('graph')} className="text-left px-3 py-2.5 rounded-lg bg-[#13131a] border border-[#1f2433] text-sm text-ink-100 hover:border-cyan/40 font-mono flex items-center gap-2 group">
                    <span className="w-1.5 h-6 rounded-full bg-cyan/40" />{n}<ChevronRight size={12} className="text-muted-dim group-hover:text-cyan ml-auto" />
                  </button>
                ))}
              </div>
            </div>
          )}
          {tab === 'graph' && (
            <div className="rounded-xl p-5 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-2">Relationship Graph</h3>
              <p className="text-xs text-muted-fg mb-4">NetworkX multi-modal visualization — click any node for intelligence panel</p>
              <button onClick={() => setTab('overview')} className="px-4 py-2 rounded-lg bg-cyan/15 text-cyan border border-cyan/30 text-xs font-mono">Open Graph Page →</button>
            </div>
          )}
          {tab === 'ai' && (
            <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-3">AI Analysis</h3>
              <div className="text-xs text-muted-fg mb-3">Phase 4 correlation engine: 8-weighted signals across synthetic dataset</div>
              <button onClick={() => setTab('overview')} className="px-4 py-2 rounded-lg bg-cyan/15 text-cyan border border-cyan/30 text-xs font-mono">Run AI Correlation →</button>
            </div>
          )}
          {tab === 'timeline' && (
            <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-3">Investigation Timeline</h3>
              <div className="space-y-3">
                {[
                  { date: '2026-08-12', event: 'Investigation opened — Operation Shadow Market', status: 'Created' },
                  { date: '2026-08-28', event: 'First correlation hit — NightTrader / DarkPhoenix', status: 'Detected' },
                  { date: '2026-09-01', event: 'Graph cluster expanded — 5 subgroups detected', status: 'Updated' },
                  { date: '2026-09-02', event: 'AI confidence 87% — high correlation confirmed', status: 'Active' },
                ].map(t => (
                  <div key={t.date} className="flex gap-3 p-3 rounded-lg bg-[#13131a] border border-[#1f2433]">
                    <div className="text-xs font-mono text-cyan shrink-0 w-24">{t.date}</div>
                    <div className="flex-1"><div className="text-sm text-ink-100">{t.event}</div></div>
                    <div className="text-[10px] font-mono text-violet">{t.status}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
          {tab === 'evidence' && (
            <div className="rounded-xl p-5" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-3">Evidence Chain</h3>
              <div className="space-y-2 text-sm text-muted-fg">
                <div className="px-3 py-2 rounded bg-[#13131a] border border-[#1f2433] font-mono">EV-2026-0142 · Forum post · NightTrader · sha256 a3f9…c0d1</div>
                <div className="px-3 py-2 rounded bg-[#13131a] border border-[#1f2433] font-mono">EV-2026-0141 · PGP key · DarkPhoenix · sha256 7b21…ee09</div>
                <div className="px-3 py-2 rounded bg-[#13131a] border border-[#1f2433] font-mono">EV-2026-0140 · Wallet · MarketEye · sha256 0x9c…aa11</div>
              </div>
            </div>
          )}
          {tab === 'report' && (
            <div className="rounded-xl p-5 text-center" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <h3 className="text-base font-semibold text-ink-100 mb-2">Generate Report</h3>
              <p className="text-xs text-muted-fg mb-4">Methodology embedded · All outputs explainable · Synthetic dataset</p>
              <button onClick={() => alert('Report generation triggered for ' + INV.id)} className="px-4 py-2 rounded-lg bg-violet/15 text-violet border border-violet/30 text-xs font-mono">Generate PDF / JSON →</button>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  )
}
