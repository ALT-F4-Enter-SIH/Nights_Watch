export default function PageHeader() {
  return (
    <div className="px-8 pt-6 pb-2 border-b" style={{ borderColor: '#1f2433' }}>
      <div className="flex items-end gap-4 mb-1">
        <h1 className="text-2xl font-bold tracking-tight text-ink-100">ShadowLink AI</h1>
        <span className="text-[10px] font-mono text-muted-dim tracking-widest2 uppercase">Phase 8 — Intelligence Shell</span>
      </div>
      <p className="text-sm text-muted-fg leading-relaxed max-w-2xl">
        Defensive synthetic identity correlation platform. Real-time graph intelligence, stylometric analysis, and behavioral clustering — built for authorized security research only.
      </p>
    </div>
  )
}
