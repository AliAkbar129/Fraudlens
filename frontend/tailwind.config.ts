import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        background: {
          DEFAULT: '#0a0a0f',
          card: 'rgba(255,255,255,0.03)',
          elevated: 'rgba(255,255,255,0.06)',
        },
        surface: 'rgba(255,255,255,0.03)',
        primary: '#00d4ff',
        success: '#00ff88',
        warning: '#ffaa00',
        danger: '#ff3366',
        text: '#e2e8f0',
        muted: '#64748b',
        border: 'rgba(255,255,255,0.06)',
      },
      fontFamily: {
        ui: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-glow': 'pulseGlow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'float': 'float 3s ease-in-out infinite',
      },
      keyframes: {
        pulseGlow: {
          '0%, 100%': { opacity: '1', boxShadow: '0 0 15px currentColor' },
          '50%': { opacity: '.5', boxShadow: '0 0 5px currentColor' },
        },
        shimmer: {
          from: { backgroundPosition: '200% 0' },
          to: { backgroundPosition: '-200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
