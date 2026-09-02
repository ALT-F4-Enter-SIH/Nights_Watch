import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Play, Pause, Repeat, ChevronDown, ChevronUp, Sparkles, ShieldCheck, Fingerprint, Network, BrainCircuit, FileText } from 'lucide-react'

const STEPS = [
  { title: 'Identity Detected', detail: 'NightTrader flagged by synthetic dataset ingestion', icon: ShieldCheck, progress: 14, evidence: 'Data ingestion complete — synthetic identity loaded' },
  { title: 'Writing Samples Analyzed', detail: 'TF-IDF + cosine over 12 synthetic text artifacts', icon: Fingerprint, progress: 28, evidence: 'Stylometric profile extracted — avg word length 5.2' },
  { title: 'High Stylometric Similarity', detail: 'Cosine similarity 0.92 — above 0.85 threshold', icon: BrainCircuit, progress: 42, evidence: 'Match detected: DarkPhoenix writing profile' },
  { title: 'Behavioral Overlap Identified', detail: 'Temporal clustering — night operations 62%', icon: Sparkles, progress: 57, evidence: 'Behavioral cluster: Night Operations' },
  { title: 'Shared PGP Fingerprint', detail: 'Exact cryptographic key match confirmed', icon: ShieldCheck, progress: 71, evidence: 'PGP fingerprint: a3f9...c0d1 — identical' },
  { title: 'Relationship Graph Updated', detail: 'NetworkX edge added — component merged', icon: Network, progress: 85, evidence: 'Graph density increased — 2 clusters → 1' },
  { title: 'AI Correlation Generated', detail: 'Weighted 8-signal score finalized', icon: Sparkles, progress: 100, evidence: 'Overall score: 0.87 — HIGH CONFIDENCE' },
]

export default function ReplayPage() {
  const [current, setCurrent] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [completed, setCompleted] = useState(false)
  const timer = useRef<NodeJS.Timeout | null>(null)

  const advance = useCallback(() => {
    setCurrent(i => {
      if (i >= STEPS.length - 1) { setPlaying(false); setCompleted(true); return i }
      return i + 1
    })
  }, [])

  useEffect(() => {
    if (playing && !completed) {
      timer.current = setTimeout(advance, 2200)
    }
    return () => { if (timer.current) clearTimeout(timer.current) }
  }, [playing, current, completed, advance])

  const restart = () => { setCurrent(0); setCompleted(false); setPlaying(false) }
  const goTo = (n: number) => { setCurrent(n); setCompleted(n >= STEPS.length - 1); setPlaying(false) }

  const s = STEPS[current]
  const Icon = s.icon

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="text-center space-y-1">
        <h2 className="text-3xl font-extrabold tracking-tight text-ink-100">Investigation Replay</h2>
        <div className="text-xs font-mono text-muted-dim">Phase 13 · Cinematic timeline · Synthetic data only</div>
      </div>

      {/* Main stage card */}
      <div className="rounded-3xl p-8 relative overflow-hidden" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04)' }}>
        {/* Gradient top line */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan via-violet to-cyan" />

        {/* Controls */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex gap-2">
            <button onClick={() => setPlaying(p => !p)} className={`px-4 py-2 rounded-xl text-sm font-mono font-bold flex items-center gap-2 transition-all ${playing ? 'bg-violet/15 text-violet border border-violet/30' : 'bg-cyan/15 text-cyan border border-cyan/30 hover:bg-cyan/25'}`}>
              {playing ? <Pause size={16}/> : <Play size={16}/>} {playing ? 'PAUSE' : 'PLAY'}
            </button>
            <button onClick={restart} className="px-4 py-2 rounded-xl text-sm font-mono bg-[#13131a] text-muted-fg border border-[#1f2433] hover:text-ink-100 hover:border-violet/40 flex items-center gap-2"><Repeat size={16}/> REPLAY</button>
          </div>
          <div className="text-xs font-mono text-cyan">Step {current + 1} / {STEPS.length}</div>
        </div>

        {/* Progress bar */}
        <div className="w-full h-2 rounded-full bg-[#181c27] mb-6 overflow-hidden">
          <motion.div className="h-full rounded-full bg-gradient-to-r from-cyan to-violet" animate={{ width: `${s.progress}%` }} transition={{ duration: 0.6, ease: [0.22,1,0.36,1] }} />
        </div>

        {/* Step display */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Left: Step info */}
          <div className="space-y-5">
            <motion.div key={current} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.35 }}>
              <div className="text-[10px] font-mono text-cyan tracking-[0.25em] uppercase mb-2">Step {current + 1}</div>
              <h3 className="text-3xl font-extrabold text-ink-100 tracking-tight mb-1">{s.title}</h3>
              <p className="text-sm text-muted-fg font-mono">{s.detail}</p>
            </motion.div>

            {/* Evidence panel */}
            <motion.div key={`${current}-ev`} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className="rounded-xl p-4" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
              <div className="text-[10px] font-mono text-violet uppercase tracking-widest mb-1">Evidence</div>
              <div className="text-sm text-ink-100 font-mono">{s.evidence}</div>
            </motion.div>
          </div>

          {/* Right: Visual icon + data */}
          <div className="flex flex-col items-center justify-center text-center space-y-3">
            <motion.div key={`icon-${current}`} initial={{ scale: 0.8, rotate: -5 }} animate={{ scale: 1, rotate: 0 }} transition={{ duration: 0.5 }} className="w-32 h-32 rounded-full flex items-center justify-center" style={{ background: '#13131a', border: '2px solid #1f2433', boxShadow: '0 0 40px rgba(6,182,212,0.15)' }}>
              <Icon size={48} className="text-cyan" />
            </motion.div>
            <div className="text-xs font-mono text-muted-fg">AI Analysis Engine · Synthetic dataset</div>
          </div>
        </div>
      </div>

      {/* Step navigation dots */}
      <div className="flex items-center justify-center gap-2 flex-wrap">
        {STEPS.map((_, i) => (
          <button key={i} onClick={() => goTo(i)} className={`w-3 h-3 rounded-full transition-all ${i === current ? 'bg-cyan shadow-[0_0_8px_rgba(6,182,212,0.5)] scale-125' : i < current ? 'bg-violet/60' : 'bg-[#181c27] hover:bg-[#1f2433]'}`} title={`Step ${i+1}`} />
        ))}
      </div>

      {/* Step cards timeline */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {STEPS.map((step, i) => {
          const active = i === current
          const done = i < current
          const StepIcon = step.icon
          return (
            <button key={i} onClick={() => goTo(i)} className={`text-left rounded-xl p-4 border transition-all ${active ? 'bg-cyan/10 border-cyan/30 shadow-[0_0_20px_rgba(6,182,212,0.08)]' : done ? 'bg-success/5 border-success/10' : 'bg-[#0f1218] border-[#1f2433] hover:border-[#2a3547]'}`}>
              <div className="flex items-center gap-2 mb-2">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center ${done ? 'bg-success text-success' : active ? 'bg-cyan text-cyan' : 'bg-[#181c27] text-muted-dim'}`}>
                  {done ? <ChevronDown size={14}/> : <StepIcon size={14}/>}<span className="sr-only">step {i+1}</span>
                </div>
                <div className="text-[10px] font-mono text-cyan">{i + 1}</div>
              </div>
              <div className={`text-sm font-medium mb-1 truncate ${active ? 'text-ink-100' : done ? 'text-success' : 'text-muted-fg'}`}>{step.title}</div>
              <div className="h-1 rounded-full bg-[#181c27] overflow-hidden"><div className={`h-full rounded-full ${done ? 'bg-violet' : active ? 'bg-cyan' : 'bg-transparent'}`} style={{ width: done ? '100%' : active ? '60%' : '0%' }} /></div>
            </button>
          )
        })}
      </div>

      {/* Final result banner */}
      <AnimatePresence>
        {completed && (
          <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6 }} className="rounded-3xl p-10 text-center relative overflow-hidden" style={{ background: 'linear-gradient(135deg, #0f1218 0%, #12142a 100%)', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 rgba(255,255,255,0.04), 0 0 60px rgba(6,182,212,0.12)' }}>
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan via-violet to-critical" />
            <div className="text-[10px] font-mono text-cyan tracking-[0.3em] uppercase mb-2">Investigation Replay Complete</div>
            <h3 className="text-5xl md:text-7xl font-extrabold tracking-tighter mb-2">
              <span className="text-transparent bg-clip-text bg-gradient-to-b from-cyan via-violet to-critical">87%</span>
            </h3>
            <div className="text-xl font-bold text-ink-100 mb-2">POTENTIAL IDENTITY LINK CONFIRMED</div>
            <div className="inline-block px-3 py-1 rounded-full text-xs font-mono font-bold bg-critical/10 text-critical border border-critical/20 mb-3">HIGH CONFIDENCE — SYNTHETIC</div>
            <div className="text-xs text-muted-fg font-mono">NightTrader ↔ DarkPhoenix · 7-step AI analysis · Human verification required</div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Disclaimer */}
      <div className="rounded-xl p-4 flex items-start gap-3" style={{ background: '#f59e0b10', border: '1px solid #f59e0b30' }}>
        <div className="text-warning"><FileText size={20} /></div>
        <div>
          <div className="text-xs font-bold text-warning tracking-widest uppercase mb-0.5">Defensive Use Only</div>
          <div className="text-xs text-ink-200 font-mono leading-relaxed">This replay demonstrates synthetic dataset analysis for authorized security research. All entities, correlations, and scores are generated from mock data. No real-world data is processed.</div>
        </div>
      </div>
    </div>
  )
}
