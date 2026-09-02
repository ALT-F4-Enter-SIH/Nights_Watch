import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import RiskBadge from '../components/ui/RiskBadge'

export default function StylometryPage() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard label="Writing Samples" value="128" sub="Indexed texts" delta="+12" deltaColor="cyan" />
        <MetricCard label="Avg Similarity" value="0.74" sub="Across pairs" delta="+0.06" deltaColor="violet" />
        <MetricCard label="High Matches" value="6" sub="Confidence ≥ 0.85" delta="+2" deltaColor="warning" />
        <MetricCard label="Model" value="MiniLM-L6" sub="384-d embeddings" delta="ONLINE" deltaColor="success" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-base font-semibold text-ink-100">Top Stylometric Matches</h2>
            <RiskBadge label="AI CONFIDENCE" level="MEDIUM" />
          </div>
          <div className="space-y-3">
            {[
              { pair: 'NightTrader · DarkPhoenix', tfidf: 0.91, semantic: 0.88, structural: 0.83, conf: 0.92 },
              { pair: 'MarketEye · TradeSense', tfidf: 0.74, semantic: 0.81, structural: 0.69, conf: 0.78 },
              { pair: 'CyberWatch · NetHunter', tfidf: 0.62, semantic: 0.58, structural: 0.71, conf: 0.65 },
            ].map((m, i) => (
              <div key={i} className="p-4 rounded-lg" style={{ background: '#13131a', border: '1px solid #1f2433' }}>
                <div className="flex items-center justify-between mb-3">
                  <div className="text-sm font-medium text-ink-100">{m.pair}</div>
                  <div className="text-xs font-mono text-cyan">{(m.conf * 100).toFixed(0)}%</div>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { label: 'TF-IDF', v: m.tidf, c: '#06b6d4' },
                    { label: 'Semantic', v: m.semantic, c: '#8b5cf6' },
                    { label: 'Structural', v: m.structural, c: '#10b981' },
                  ].map(s => (
                    <div key={s.label}>
                      <div className="flex justify-between text-[10px] mb-1">
                        <span className="text-muted-fg">{s.label}</span>
                        <span className="font-mono text-ink-200">{(s.v * 100).toFixed(0)}%</span>
                      </div>
                      <div className="h-1.5 rounded-full overflow-hidden" style={{ background: '#181c27' }}>
                        <div className="h-full rounded-full" style={{ width: `${s.v * 100}%`, background: s.c }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl p-6" style={{ background: '#0f1218', border: '1px solid #1f2433', boxShadow: 'inset 0 1px 0 0 rgba(255,255,255,0.04)' }}>
          <h2 className="text-base font-semibold text-ink-100 mb-4">Signal Weights</h2>
          <div className="space-y-3">
            {[
              { label: 'TF-IDF Cosine', val: 90 },
              { label: 'Sentence Embeddings', val: 85 },
              { label: 'N-gram Overlap', val: 70 },
              { label: 'Punctuation Profile', val: 55 },
              { label: 'Avg Sentence Length', val: 40 },
            ].map(s => (
              <div key={s.label}>
                <div className="flex justify-between text-[11px] mb-1">
                  <span className="text-muted-fg">{s.label}</span>
                  <span className="font-mono text-[11px] text-ink-200">{s.val}%</span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden" style={{ background: '#181c27' }}>
                  <div className="h-full rounded-full bg-violet/80" style={{ width: `${s.val}%`, background: '#8b5cf6' }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
