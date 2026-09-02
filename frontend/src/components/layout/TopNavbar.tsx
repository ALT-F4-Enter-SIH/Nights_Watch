import { Bell, Search, Command, Activity } from 'lucide-react'

export default function TopNavbar() {
  return (
    <header
      className="fixed top-0 right-0 h-[4.5rem] z-20 flex items-center px-6 gap-4"
      style={{
        left: 224,
        background: 'rgba(10, 12, 18, 0.85)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderBottom: '1px solid #1f2433',
      }}
    >
      {/* Search */}
      <div className="flex-1 max-w-xl">
        <div
          className="flex items-center gap-2 px-3 h-9 rounded-md"
          style={{ background: '#0f1218', border: '1px solid #1f2433' }}
        >
          <Search size={14} className="text-muted-dim" />
          <input
            type="text"
            placeholder="Search identities, wallets, fingerprints…"
            className="flex-1 bg-transparent outline-none text-[13px] text-ink-200 placeholder:text-muted-dim"
          />
          <span className="flex items-center gap-1 text-[10px] text-muted-dim font-mono">
            <Command size={10} />K
          </span>
        </div>
      </div>

      {/* Status indicator */}
      <div className="flex items-center gap-2 text-[11px] text-muted-fg font-mono tracking-wide2">
        <Activity size={12} className="text-success" />
        <span>47 NODES</span>
        <span className="text-line-strong">·</span>
        <span>112 EDGES</span>
      </div>

      {/* Notifications */}
      <button
        className="relative w-9 h-9 flex items-center justify-center rounded-md text-muted-fg hover:text-ink-200 transition-colors"
        style={{ background: '#0f1218', border: '1px solid #1f2433' }}
        aria-label="Notifications"
      >
        <Bell size={14} />
        <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-critical" />
      </button>

      {/* User avatar */}
      <div className="flex items-center gap-2.5 pl-3 border-l" style={{ borderColor: '#1f2433' }}>
        <div
          className="w-8 h-8 rounded-full flex items-center justify-center text-[11px] font-semibold text-ink-900"
          style={{ background: 'linear-gradient(135deg, #22d3ee, #a78bfa)' }}
        >
          OP
        </div>
        <div className="leading-tight">
          <div className="text-[12px] font-medium text-ink-200">Operator</div>
          <div className="text-[10px] text-muted-dim tracking-wider2">ANALYST</div>
        </div>
      </div>
    </header>
  )
}
