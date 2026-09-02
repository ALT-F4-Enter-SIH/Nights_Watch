/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Deep layered intelligence surfaces
        ink: {
          900: '#06070b',
          800: '#0a0c12',
          700: '#0f1218',
          600: '#141822',
          500: '#1a1f2c',
          400: '#222837',
        },
        line: {
          DEFAULT: '#1f2433',
          soft: '#181c27',
          strong: '#2a3142',
        },
        // Accent palette
        cyan: {
          glow: '#22d3ee',
          DEFAULT: '#06b6d4',
          deep: '#0e7490',
        },
        violet: {
          glow: '#a78bfa',
          DEFAULT: '#8b5cf6',
          deep: '#6d28d9',
        },
        success: '#10b981',
        warning: '#f59e0b',
        critical: '#ef4444',
        muted: {
          DEFAULT: '#6b7280',
          fg: '#94a3b8',
          dim: '#475569',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      letterSpacing: {
        wider2: '0.08em',
        widest2: '0.14em',
      },
      boxShadow: {
        'inner-line': 'inset 0 1px 0 0 rgba(255,255,255,0.04)',
        'panel': '0 1px 0 0 rgba(255,255,255,0.04) inset, 0 30px 60px -20px rgba(0,0,0,0.5)',
        'glow-cyan': '0 0 0 1px rgba(34,211,238,0.18), 0 0 24px -6px rgba(34,211,238,0.18)',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-400px 0' },
          '100%': { backgroundPosition: '400px 0' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.4)' },
        },
      },
      animation: {
        shimmer: 'shimmer 1.6s linear infinite',
        pulseDot: 'pulseDot 1.6s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
