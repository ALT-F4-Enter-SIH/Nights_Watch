import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Wand2, ShieldCheck, Fingerprint, Wallet, Network, Sparkles, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'

const STEPS = [
  { label: 'Initializing AI Analysis', detail: 'Loading correlation engine', icon: Wand2, duration: 1200 },
  { label: 'Analyzing writing fingerprints', detail: 'TF-IDF + cosine similarity', icon: Fingerprint, duration: 1400 },
  { label: 'Processing behavioral patterns', detail: 'Time-series + cluster matching', icon: Sparkles, duration: 1200 },
  { label: 'Cross-referencing cryptographic identifiers', detail: 'PGP fingerprint comparison', icon: ShieldCheck, duration: 900 },
  { label: 'Analyzing wallet relationships', detail: 'Address prefix + transaction graph', icon: Wallet, duration: 1000 },
  { label: 'Analyzing relationship graph', detail: 'NetworkX connected components', icon: Network, duration: 1100 },
  { label: 'Finalizing confidence score', detail: 'Weighted aggregation', icon: Wand2, duration: 900 },
]

const SIGNALS = [
  { label: 'Stylometry', score: 92, color: '#06b6d4' },
  { label: 'Behavior', score: 78, color: '#8b5cf6' },
  { label: 'PGP', score: 100, color: '#f59e0b' },
  { label: 'Wallet', score: 65, color: '#10b981' },
  { label: 'Metadata', score: 81, color: '#f43f5e' },
]

const REASONS = [
  'Shared PGP fingerprint — exact key match confirmed',
  'Strong writing similarity — stylometric cosine 0.92',
  'Behavioral overlap — temporal patterns aligned',
  'Related network connections — 3 shared clusters',
]

export default function CorrelationPage() {
  const [a, setA] = useState('NightTrader')
  const [b, setB] = useState('DarkPhoenix')
  const [running, setRunning] = useState(false)
  const [stepIdx, setStepIdx] = useState(-1)
  const [done, setDone] = useState(false)
  const [showWhy, setShowWhy] = useState(false)
  const timer = useRef<NodeJS.Timeout | null>(null)

  function run() {
    if (running) return
    setRunning(true)
    setDone(false)
    setShowWhy(false)
    setStepIdx(0)

    let i = 0
    const advance = () => {
      i++
      if (i >= STEPS.length) {
        setRunning(false)
        setDone(true)
        return
      }
      setStepIdx(i)
      timer.current = setTimeout(advance, STEPS[i].duration)
    }
    timer.current = setTimeout(advance, STEPS[0].duration)
  }

  useEffect(() => () => { if (timer.current) clearTimeout(timer.current) }, [])

  const current = stepIdx >= 0 ? STEPS[stepIdx] : null
  const Icon = current?.icon ?? Wand2

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Header */}
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-extrabold tracking-tight text-ink-100">AI Correlation Engine</h2>
        <p className="text-sm text-muted-fg font-mono">Phase 11 · Synthetic dataset only · Human verification required</p>
      </div>

      {/* Inputs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 items-end">
        <div>
          <label className="text-[10px] font-mono text-muted-dim uppercase mb-1">Identity A</label>
          <input value={a} onChange={e => setA(e.target.value)} className="w-full px-3 py-2.5 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-sm text-ink-100 font-mono focus:outline-none focus:border-cyan/60" />
        </div>
        <div>
          <label className="text-[10px] font-mono text-muted-dim uppercase mb-1">Identity B</label>
          <input value={b} onChange={e => setB(e.target.value)} className="w-full px-3 py-2.5 rounded-lg bg-[#0a0c12] border border-[#1f2433] text-sm text-ink-100 font-mono focus:outline-none focus:border-cyan/60" />
        </div>
        <button onClick={run} disabled={running} className={`px-6 py-2.5 rounded-lg text-sm font-mono font-bold transition-all ${running ? 'bg-[#13131a] text-muted-fg border border-[#1f2433]' : 'bg-cyan/15 text-cyan border border-cyan/30 hover:bg-cyan/25 shadow-[0_0_30px_rgba(6,182,212,0.15)]'}`}>
          {running ? 'ANALYZING...' : 'RUN AI CORRELATION'}
        </button>
      </div>

      {/* Analysis Sequence */}
      <AnimatePresence>
        {running && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
            <div className="rounded-2xl p-6 space-y-5" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)' }}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Left: Step list */}
                <div className="space-y-2">
                  {STEPS.map((s, i) => {
                    const active = i === stepIdx
                    const doneStep = i < stepIdx
                    const StepIcon = s.icon
                    return (
                      <div key={i} className={`flex items-center gap-3 rounded-lg px-3 py-2.5 transition-all ${active ? 'bg-cyan/10 border border-cyan/20' : doneStep ? 'bg-success/5 border border-success/10' : 'bg-[#13131a] border border-transparent'}`}>
                        <div className={`w-7 h-7 rounded-full flex items-center justify-center shrink-0 ${active ? 'bg-cyan text-cyan' : doneStep ? 'bg-success text-success' : 'bg-[#181c27] text-muted-dim'}`}>
                          {doneStep ? <Sparkles size={14}/> : active ? <StepIcon size={14}/> : <span className="text-[10px] font-mono">{i+1}</span>}
                        </div>
                        <div className="min-w-0 flex-1">
                          <div className={`text-sm font-medium truncate ${active ? 'text-ink-100' : doneStep ? 'text-success' : 'text-muted-fg'}`}>{s.label}</div>
                          <div className="text-[10px] font-mono text-muted-dim">{s.detail}</div>
                        </div>
                        {active && <motion.div animate={{ scale: [1, 1.2, 1] }} transition={{ repeat: Infinity, duration: 1 }} className="w-1.5 h-1.5 rounded-full bg-cyan" />}
                      </div>
                    )
                  })}
                </div>
                {/* Right: Progress + detail */}
                <div className="flex flex-col items-center justify-center text-center space-y-3">
                  <div className="w-32 h-32 rounded-full flex items-center justify-center" style={{ border: '3px solid #1f2433', background: '#13131a' }}>
                    <motion.div
                      key={current?.label ?? 'idle'}
                      initial={{ scale: 0.8, opacity: 0.5 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.35 }}
                      className="text-center"
                    >
                      <Icon size={36} className="text-cyan mx-auto mb-2" />
                      <div className="text-xs font-mono text-cyan">{current?.label ?? 'Waiting...'}</div>
                    </motion.div>
                  </div>
                  <div className="w-full h-3 rounded-full overflow-hidden bg-[#181c27]">
                    <motion.div
                      className="h-full bg-gradient-to-r from-cyan to-violet rounded-full"
                      initial={{ width: '0%' }}
                      animate={{ width: `${((stepIdx + 1) / STEPS.length) * 100}%` }}
                      transition={{ duration: 0.4 }}
                    />
                  </div>
                  <div className="text-xs font-mono text-muted-fg">{Math.round(((stepIdx + 1) / STEPS.length) * 100)}% complete</div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Dramatic Reveal */}
      <AnimatePresence>
        {done && (
          <motion.div initial={{ opacity: 0, y: 40, scale: 0.98 }} animate={{ opacity: 1, y: 0, scale: 1 }} transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }} className="space-y-8">
            {/* Big score */}
            <div className="rounded-3xl p-10 text-center relative overflow-hidden" style={{ background: 'linear-gradient(135deg, #0f1218 0%, #12142a 100%)', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04), 0 0 60px rgba(6,182,212,0.08)' }}>
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan via-violet to-cyan" />
              <div className="text-[10px] font-mono text-cyan tracking-[0.3em] uppercase mb-3">AI Correlation Result</div>
              <div className="text-7xl md:text-9xl font-extrabold tracking-tighter leading-none mb-2">
                <span className="text-transparent bg-clip-text bg-gradient-to-b from-cyan via-violet to-cyan">87%</span>
              </div>
              <div className="text-xl font-bold text-ink-100 mb-1">POTENTIAL IDENTITY CORRELATION</div>
              <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold tracking-widest bg-critical/10 text-critical border border-critical/20">HIGH CONFIDENCE</div>
              <div className="text-xs text-muted-fg font-mono mt-3">{a} ↔ {b} · Weighted mult-signal score</div>
            </div>

            {/* Signals */}
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {SIGNALS.map(s => (
                <motion.div
                  key={s.label}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.05 * SIGNALS.indexOf(s) }}
                  className="rounded-xl p-4 text-center"
                  style={{ background: '#0f1218', border: '1px solid #1f2433' }}
                >
                  <div className="text-xs font-mono text-muted-dim mb-2">{s.label}</div>
                  <div className="text-3xl font-extrabold text-ink-100 tracking-tight">{s.score}%</div>
                  <div className="h-1.5 rounded-full bg-[#181c27] mt-3 overflow-hidden">
                    <motion.div initial={{ width: 0 }} animate={{ width: `${s.score}%` }} transition={{ delay: 0.3 + 0.08 * SIGNALS.indexOf(s), duration: 0.8, ease: [0.22, 1, 0.36, 1] }} className="h-full rounded-full" style={{ background: s.color }} />
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Why this result */}
            <div className="rounded-2xl p-6 space-y-4" style={{ background: '#0f1218', border: '1px solid #1f2433' }}>
              <button onClick={() => setShowWhy(!showWhy)} className="flex items-center gap-2 text-sm font-mono text-cyan hover:text-ink-100 transition-colors">
                <ChevronDown size={16} className={`transition-transform ${showWhy ? 'rotate-180' : ''}`} /> WHY THIS RESULT?
              </button>
              <AnimatePresence>
                {showWhy && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="overflow-hidden">
                    <div className="space-y-2 pt-2">
                      {REASONS.map((r, i) => (
                        <div key={i} className="flex items-center gap-3 rounded-lg px-3 py-2.5 bg-[#13131a] border border-[#1f2433] text-sm text-ink-100">
                          <div className="w-5 h-5 rounded-full bg-cyan/10 text-cyan flex items-center justify-center shrink-0 text-xs font-bold">{i + 1}</div>
                          <span className="font-mono text-xs">{r}</span>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Disclaimer */}
            <div className="rounded-xl p-4 flex items-start gap-3" style={{ background: '#f59e0b10', border: '1px solid #f59e0b30' }}>
              <AlertTriangle className="text-warning shrink-0 mt-0.5" size={20} />
              <div>
                <div className="text-xs font-bold text-warning tracking-widest uppercase mb-0.5">Disclaimer</div>
                <div className="text-xs text-ink-200 font-mono leading-relaxed">AI-Generated Analytical Hypothesis — Human Verification Required. This result is synthesized from the mock dataset for defensive security research only. No real-world deanonymization is performed. Confirm all findings with authorized analysts before any action.</div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
