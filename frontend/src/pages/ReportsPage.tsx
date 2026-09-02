import { useState } from 'react'
import { motion } from 'framer-motion'
import { Download, FileText, Printer, ShieldCheck, AlertTriangle, BarChart3, Fingerprint, BrainCircuit, Network, Lock } from 'lucide-react'

const REPORT = {
  id: 'INV-2026-001',
  title: 'OPERATION SHADOW MARKET',
  generated: new Date().toISOString().slice(0, 10),
  analyst: 'Agent K',
  entities: 24,
  correlations: 18,
  avgConfidence: 0.78,
  riskLevel: 'HIGH',
}

export default function ReportsPage() {
  const [exported, setExported] = useState('')

  function downloadJSON() {
    const blob = new Blob([JSON.stringify({ ...REPORT, sections: ['executive','entities','correlation','relationships','evidence','risk','limitations','disclaimer'] })], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `shadowlink-report-${REPORT.id}.json`; a.click()
    URL.revokeObjectURL(url)
    setExported('JSON downloaded')
    setTimeout(() => setExported(''), 2000)
  }

  function downloadCSV() {
    const rows = [
      ['Investigation ID', REPORT.id],
      ['Title', REPORT.title],
      ['Status', REPORT.riskLevel],
      ['Generated', REPORT.generated],
      ['Analyst', REPORT.analyst],
      ['Entities', REPORT.entities],
      ['Correlations', REPORT.correlations],
      ['Avg Confidence', REPORT.avgConfidence.toFixed(2)],
    ]
    const csv = rows.map(r => r.join(',')).join('\n')
    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `shadowlink-report-${REPORT.id}.csv`; a.click()
    URL.revokeObjectURL(url)
    setExported('CSV downloaded')
    setTimeout(() => setExported(''), 2000)
  }

  const print = () => window.print()

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="text-[10px] font-mono text-cyan tracking-widest uppercase mb-1">SHADOWLINK AI</div>
          <h2 className="text-3xl font-extrabold text-ink-100 tracking-tight">THREAT INTELLIGENCE REPORT</h2>
          <div className="text-xs font-mono text-muted-fg mt-1">Investigation {REPORT.id} · Generated {REPORT.generated} · Analyst {REPORT.analyst}</div>
        </div>
        <div className="flex gap-2">
          <button onClick={downloadJSON} className="px-3 py-2 rounded-lg bg-cyan/15 text-cyan text-xs font-mono border border-cyan/30 hover:bg-cyan/25 flex items-center gap-1.5"><Download size={14}/> JSON</button>
          <button onClick={downloadCSV} className="px-3 py-2 rounded-lg bg-violet/15 text-violet text-xs font-mono border border-violet/30 hover:bg-violet/25 flex items-center gap-1.5"><Download size={14}/> CSV</button>
          <button onClick={print} className="px-3 py-2 rounded-lg bg-[#13131a] text-muted-fg text-xs font-mono border border-[#1f2433] hover:text-ink-100 flex items-center gap-1.5"><Printer size={14}/> Print</button>
        </div>
      </div>
      {exported && <div className="text-xs font-mono text-cyan">{exported}</div>}

      {/* Report card */}
      <div className="rounded-2xl p-8 space-y-7" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)' }}>
        {/* Executive Summary */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><ShieldCheck size={18} className="text-cyan"/> EXECUTIVE SUMMARY</h3>
          <p className="text-sm text-ink-100 leading-relaxed">This report presents findings from <strong>Operation Shadow Market</strong> (INV-2026-001), an AI-powered correlation study of synthetic identity clusters. The investigation identified <strong>18 high-confidence correlations</strong> across 24 mapped entities, with an average AI confidence score of <strong>78%</strong>. Key findings include shared cryptographic fingerprints, strong stylometric similarity (0.92 cosine), behavioral overlap in night-operation patterns, and integrated network clusters. All results are analytical hypotheses derived from synthetic mock data for defensive security research only.</p>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* Entity Analysis */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><Fingerprint size={18} className="text-violet"/> ENTITY ANALYSIS</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { name: 'NightTrader', risk: 0.94, type: 'Identity', links: 6 },
              { name: 'DarkPhoenix', risk: 0.91, type: 'Identity', links: 5 },
              { name: 'MarketEye', risk: 0.73, type: 'Identity', links: 4 },
              { name: 'TradeSense', risk: 0.62, type: 'Identity', links: 3 },
            ].map(e => (
              <div key={e.name} className="rounded-lg p-3 bg-[#13131a] border border-[#1f2433]">
                <div className="text-xs font-mono text-cyan">{e.type}</div>
                <div className="text-sm font-bold text-ink-100">{e.name}</div>
                <div className="text-xs text-muted-fg">Risk {e.risk.toFixed(2)} · {e.links} links</div>
                <div className="h-1 rounded-full bg-[#181c27] mt-2 overflow-hidden"><div className="h-full rounded-full bg-cyan/80" style={{ width: `${e.risk*100}%` }}/></div>
              </div>
            ))}
          </div>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* AI Correlation Results */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><BrainCircuit size={18} className="text-violet"/> AI CORRELATION RESULTS</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div className="rounded-lg p-4 bg-[#13131a] border border-[#1f2433]">
              <div className="text-xs font-mono text-muted-dim">Overall Score</div>
              <div className="text-3xl font-extrabold text-cyan">87%</div>
              <div className="text-xs text-muted-fg">Weighted 8-signal aggregate</div>
            </div>
            <div className="rounded-lg p-4 bg-[#13131a] border border-[#1f2433]">
              <div className="text-xs font-mono text-muted-dim">Confidence Distribution</div>
              <div className="flex gap-2 mt-1">
                <span className="text-xs font-mono text-cyan">High: 34</span>
                <span className="text-xs font-mono text-violet">Medium: 41</span>
                <span className="text-xs font-mono text-muted-fg">Low: 37</span>
              </div>
            </div>
          </div>
          <div className="mt-3 text-xs text-muted-fg font-mono">Signals: Stylometry 92% · Behavior 78% · PGP 100% · Wallet 65% · Metadata 81%</div>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* Key Relationships */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><Network size={18} className="text-success"/> KEY RELATIONSHIPS</h3>
          <table className="w-full text-sm">
            <thead><tr className="text-left text-[10px] font-mono text-muted-dim uppercase"><th className="py-2 px-2">Pair</th><th className="py-2 px-2">Type</th><th className="py-2 px-2">Confidence</th><th className="py-2 px-2">Evidence</th></tr></thead>
            <tbody>
              {[
                { pair: 'NightTrader ↔ DarkPhoenix', type: 'PGP + Stylometry', conf: 0.92, ev: 'Exact fingerprint + writing similarity' },
                { pair: 'MarketEye ↔ TradeSense', type: 'Behavioral', conf: 0.78, ev: 'Shared night operation patterns' },
                { pair: 'CyberWatch ↔ NetHunter', type: 'Infrastructure', conf: 0.65, ev: 'Common IP origin range' },
              ].map(r => (
                <tr key={r.pair} className="border-t border-[#1f2433]"><td className="py-2 px-2 font-mono text-ink-100">{r.pair}</td><td className="py-2 px-2 text-muted-fg">{r.type}</td><td className="py-2 px-2 font-mono text-cyan">{(r.conf*100).toFixed(0)}%</td><td className="py-2 px-2 text-xs text-muted-fg">{r.ev}</td></tr>
              ))}
            </tbody>
          </table>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* Evidence */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><Lock size={18} className="text-violet"/> EVIDENCE</h3>
          <div className="space-y-2">
            {[
              { id: 'EV-2026-0142', type: 'Forum post', source: 'NightTrader', hash: 'a3f9...c0d1', status: 'Sealed' },
              { id: 'EV-2026-0141', type: 'PGP key', source: 'DarkPhoenix', hash: '7b21...ee09', status: 'Verified' },
              { id: 'EV-2026-0140', type: 'Wallet addr', source: 'MarketEye', hash: '0x9c...aa11', status: 'Pending' },
            ].map(e => (
              <div key={e.id} className="flex items-center gap-3 p-3 rounded-lg bg-[#13131a] border border-[#1f2433] text-xs font-mono">
                <div className="w-1.5 h-8 rounded-full bg-violet/40 shrink-0" />
                <div className="flex-1"><div className="text-ink-100">{e.id} · {e.type}</div><div className="text-muted-fg">{e.source} · sha256 {e.hash}</div></div>
                <div className="text-violet">{e.status}</div>
              </div>
            ))}
          </div>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* Risk Indicators */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-3 flex items-center gap-2"><BarChart3 size={18} className="text-warning"/> RISK INDICATORS</h3>
          <div className="flex gap-2 flex-wrap">
            {['Critical: 4', 'High: 9', 'Medium: 16', 'Low: 18'].map(r => (
              <span key={r} className="px-2 py-1 rounded-md bg-[#13131a] border border-[#1f2433] text-xs font-mono text-ink-100">{r}</span>
            ))}
          </div>
        </section>
        <hr style={{ borderColor: '#1f2433' }} />

        {/* Limitations */}
        <section>
          <h3 className="text-lg font-bold text-ink-100 mb-2 flex items-center gap-2"><AlertTriangle size={18} className="text-warning"/> LIMITATIONS</h3>
          <ul className="list-disc pl-5 text-sm text-muted-fg space-y-1 leading-relaxed">
            <li>All data is synthetic and generated for defensive research only.</li>
            <li>AI correlations are statistical hypotheses, not confirmed identities.</li>
            <li>Graph algorithms use synthetic dataset — no real-world scanning performed.</li>
            <li>Evidence items are mock artifacts — no real legal admissibility.</li>
          </ul>
        </section>

        {/* Disclaimer */}
        <section className="rounded-xl p-5" style={{ background: '#f59e0b10', border: '1px solid #f59e0b30' }}>
          <div className="flex items-start gap-3">
            <AlertTriangle className="text-warning shrink-0 mt-0.5" size={20} />
            <div>
              <div className="text-sm font-bold text-warning tracking-widest uppercase mb-1">DISCLAIMER</div>
              <p className="text-xs text-ink-200 font-mono leading-relaxed">AI-generated correlations are analytical hypotheses and require human verification. No unauthorized scanning, exploitation, or deanonymization occurs. This report is for authorized defensive security research, educational demonstration, and synthetic dataset analysis only.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
