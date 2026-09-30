import React from 'react';
import GlassCard from '../ui/GlassCard';

export const RiskHeatmap: React.FC = () => {
  // A simple grid-based heatmap using divs since recharts heatmap is tricky to set up perfectly without extra dependencies
  const channels = ['Web', 'Mobile App', 'POS', 'ATM', 'Agent'];
  const types = ['Purchase', 'Transfer', 'Withdrawal', 'Deposit', 'Bill Pay'];
  
  const generateIntensity = (type: string, channel: string) => {
    // Fake some high risk areas
    if (type === 'Transfer' && channel === 'Web') return 0.85;
    if (type === 'Withdrawal' && channel === 'ATM') return 0.6;
    if (type === 'Purchase' && channel === 'POS') return 0.1;
    return Math.random() * 0.4 + 0.1;
  };

  const getColor = (intensity: number) => {
    if (intensity > 0.8) return `rgba(255, 51, 102, ${intensity})`; // Danger
    if (intensity > 0.5) return `rgba(255, 170, 0, ${intensity})`; // Warning
    return `rgba(0, 212, 255, ${intensity})`; // Primary
  };

  return (
    <GlassCard className="h-full flex flex-col p-4">
      <h3 className="font-semibold text-lg mb-4">Risk by Channel & Type</h3>
      <div className="flex-1 flex flex-col">
        <div className="flex h-8">
          <div className="w-24"></div>
          {channels.map(c => (
            <div key={c} className="flex-1 text-center text-xs text-slate-400 flex items-center justify-center font-medium">{c}</div>
          ))}
        </div>
        <div className="flex-1 flex flex-col gap-1">
          {types.map(t => (
            <div key={t} className="flex-1 flex gap-1 items-center">
              <div className="w-24 text-xs text-slate-400 font-medium truncate pr-2 text-right">{t}</div>
              {channels.map(c => {
                const intensity = generateIntensity(t, c);
                return (
                  <div
                    key={c}
                    className="flex-1 h-full rounded flex items-center justify-center text-[10px] font-mono group relative cursor-crosshair transition-colors hover:border hover:border-white/50"
                    style={{ backgroundColor: getColor(intensity) }}
                  >
                    <span className="opacity-0 group-hover:opacity-100 text-white font-bold bg-black/50 px-1 py-0.5 rounded backdrop-blur-sm">
                      {(intensity * 100).toFixed(0)}
                    </span>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>
    </GlassCard>
  );
};

export default RiskHeatmap;
