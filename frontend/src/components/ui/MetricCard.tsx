interface Props {
  label: string
  value: string
  sub?: string
  delta?: string
  deltaColor?: 'cyan' | 'purple' | 'success' | 'warning' | 'critical'
}

export default function MetricCard({ label, value, sub, delta, deltaColor = 'cyan' }: Props) {
  const deltaMap = {
    cyan: 'text-cyan',
    purple: 'text-violet',
    success: 'text-success',
    warning: 'text-warning',
    critical: 'text-critical',
  }
  return (
    <div
      className="rounded-xl p-5 transition-all duration-200 hover:-translate-y-0.5"
      style={{
        background: '#0f1218',
        border: '1px solid #1f2433',
        boxShadow: '0 1px 0 0 rgba(255,255,255,0.03) inset',
      }}
    >
      <div className="text-[11px] font-mono tracking-wider2 text-muted-dim uppercase mb-2">{label}</div>
      <div className="text-2xl font-semibold text-ink-100 tracking-tight">{value}</div>
      {delta && (
        <div className={`text-xs font-medium mt-1 ${deltaMap[deltaColor]}`}>{delta}</div>
      )}
      {sub && <div className="text-[11px] text-muted-fg mt-2">{sub}</div>}
    </div>
  )
}
