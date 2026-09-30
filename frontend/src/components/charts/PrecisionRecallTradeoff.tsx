import React, { useState } from 'react';
import GlassCard from '../ui/GlassCard';

export const PrecisionRecallTradeoff: React.FC = () => {
  const [threshold, setThreshold] = useState(0.5);
  const precision = Math.min(1, 0.5 + threshold * 0.5);
  const recall = Math.max(0, 1 - Math.pow(threshold, 2));

  return (
    <GlassCard className="h-full w-full p-6 flex flex-col justify-center">
      <h3 className="font-semibold text-lg mb-6 text-white text-center">Precision vs Recall</h3>
      
      <div className="flex justify-between px-8 mb-8 relative">
        <div className="text-center">
          <div className="text-3xl font-bold font-mono text-primary">{(precision * 100).toFixed(1)}%</div>
          <div className="text-xs text-slate-400 mt-1 uppercase tracking-widest">Precision</div>
        </div>
        
        <div className="w-px bg-white/10 mx-4"></div>
        
        <div className="text-center">
          <div className="text-3xl font-bold font-mono text-success">{(recall * 100).toFixed(1)}%</div>
          <div className="text-xs text-slate-400 mt-1 uppercase tracking-widest">Recall</div>
        </div>
      </div>
      
      <div className="px-4">
        <div className="flex justify-between text-xs text-slate-500 mb-2">
          <span>Catch More (Low Threshold)</span>
          <span>More Accurate (High Threshold)</span>
        </div>
        <input 
          type="range" 
          min="0" max="1" step="0.01" 
          value={threshold} 
          onChange={(e) => setThreshold(parseFloat(e.target.value))}
          className="w-full accent-primary" 
        />
        <div className="text-center text-xs text-slate-400 mt-2 font-mono">
          Current Threshold: {threshold.toFixed(2)}
        </div>
      </div>
    </GlassCard>
  );
};

export default PrecisionRecallTradeoff;
