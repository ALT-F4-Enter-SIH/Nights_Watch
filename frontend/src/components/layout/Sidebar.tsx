import { useState, useCallback } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard,
  Search,
  GitFork,
  Brain,
  Type,
  Activity,
  Server,
  Lock,
  FileText,
  Settings,
  ChevronLeft,
  ChevronRight,
  Shield,
  Eye,
  Play,
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/', label: 'Overview', icon: LayoutDashboard },
  { to: '/investigations', label: 'Investigations', icon: Search },
  { to: '/graph', label: 'Identity Graph', icon: GitFork },
  { to: '/correlation', label: 'AI Correlation', icon: Brain },
  { to: '/stylometry', label: 'Stylometry Lab', icon: Type },
  { to: '/behavior', label: 'Behavioral Intelligence', icon: Activity },
  { to: '/infrastructure', label: 'Infrastructure Intel', icon: Server },
  { to: '/evidence', label: 'Evidence Vault', icon: Lock },
  { to: '/reports', label: 'Reports', icon: FileText },
  { to: '/replay', label: 'Investigation Replay', icon: Play },
  { divider: true },
  { to: '/settings', label: 'Settings', icon: Settings },
]

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false)
  const location = useLocation()

  const toggle = useCallback(() => setCollapsed(c => !c), [])

  return (
    <motion.aside
      animate={{ width: collapsed ? 64 : 224 }}
      transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
      className="fixed left-0 top-0 h-screen z-30 flex flex-col"
      style={{
        background: 'linear-gradient(180deg, #0c0e16 0%, #0a0c12 100%)',
        borderRight: '1px solid #1f2433',
      }}
    >
      {/* Logo */}
      <div className="flex items-center h-14 px-4 gap-3 border-b" style={{ borderColor: '#1f2433' }}>
        <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style={{ background: 'linear-gradient(135deg, #06b6d4, #8b5cf6)' }}>
          <Shield size={16} className="text-white" />
        </div>
        <AnimatePresence>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.15 }}
              className="overflow-hidden"
            >
              <span className="text-sm font-semibold tracking-wide2 whitespace-nowrap text-cyan">
                SHADOWLINK
              </span>
              <span className="block text-[10px] text-muted-dim tracking-widest2 -mt-0.5">AI INTELLIGENCE</span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Status dot */}
      <div className="px-4 py-2.5 flex items-center gap-2 border-b" style={{ borderColor: '#1f2433' }}>
        <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulseDot shrink-0" />
        <AnimatePresence>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.15 }}
              className="text-[11px] text-muted-fg tracking-wide2 whitespace-nowrap"
            >
              SYSTEM ACTIVE
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      {/* Nav items */}
      <nav className="flex-1 overflow-y-auto overflow-x-hidden py-3 px-2 space-y-0.5">
        {NAV_ITEMS.map((item, i) =>
          'divider' in item ? (
            <div key={`div-${i}`} className="h-px mx-1 my-3" style={{ background: '#1f2433' }} />
          ) : (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
            >
              {({ isActive }) => (
                <motion.div
                  whileHover={{ x: 2 }}
                  transition={{ duration: 0.15 }}
                  className={[
                    'flex items-center gap-3 rounded-md px-2 py-2.5 text-[13px] font-medium transition-all duration-150',
                    collapsed ? 'justify-center' : '',
                    isActive
                      ? 'text-cyan'
                      : 'text-muted-fg hover:text-ink-400',
                  ].join(' ')}
                  style={
                    isActive
                      ? {
                          background: 'rgba(6,182,212,0.07)',
                          borderLeft: '2px solid #06b6d4',
                          borderRadius: '6px',
                        }
                      : {}
                  }
                >
                  <item.icon size={17} className="shrink-0" />
                  {!collapsed && <span className="whitespace-nowrap">{item.label}</span>}
                </motion.div>
              )}
            </NavLink>
          )
        )}
      </nav>

      {/* Collapse toggle */}
      <button
        onClick={toggle}
        className="flex items-center justify-center h-10 border-t text-muted-dim hover:text-muted-fg transition-colors"
        style={{ borderColor: '#1f2433' }}
        aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
      </button>
    </motion.aside>
  )
}
