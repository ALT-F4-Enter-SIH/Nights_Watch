/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'sl-bg': '#0a0a0f',
        'sl-surface': '#13131a',
        'sl-surface-2': '#1c1c26',
        'sl-border': '#2a2a36',
        'sl-accent': '#6366f1',
        'sl-text': '#e5e5e5',
        'sl-text-dim': '#a0a0b0',
        'sl-success': '#10b981',
        'sl-warning': '#f59e0b',
        'sl-danger': '#ef4444',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
