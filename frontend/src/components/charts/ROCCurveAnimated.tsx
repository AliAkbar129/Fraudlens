import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../ui/GlassCard';

export const ROCCurveAnimated: React.FC = () => {
  const [drawn, setDrawn] = useState(false);
  const [threshold, setThreshold] = useState(0.5);

  useEffect(() => {
    setDrawn(true);
  }, []);

  // Simple mock ROC curve path
  const pathData = "M 0 300 Q 50 50 300 0";
  
  // Calculate point on curve based on threshold (simplified)
  const px = threshold * 300;
  const py = 300 - Math.sqrt(px/300) * 300;

  return (
    <GlassCard className="h-full w-full p-6 flex flex-col">
      <h3 className="font-semibold text-lg mb-2 text-white">ROC Curve (AUC: 0.94)</h3>
      <div className="flex-1 relative flex items-center justify-center">
        <svg width="100%" height="100%" viewBox="-20 -20 340 340" className="overflow-visible">
          {/* Axes */}
          <line x1="0" y1="300" x2="300" y2="300" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
          <line x1="0" y1="300" x2="0" y2="0" stroke="rgba(255,255,255,0.2)" strokeWidth="2" />
          
          {/* Diagonal Reference */}
          <line x1="0" y1="300" x2="300" y2="0" stroke="rgba(255,255,255,0.1)" strokeDasharray="5 5" strokeWidth="2" />
          
          {/* Gradient Fill under curve */}
          <linearGradient id="rocGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#00d4ff" stopOpacity={0} />
          </linearGradient>
          
          <motion.path 
            d={`${pathData} L 300 300 Z`} 
            fill="url(#rocGradient)"
            initial={{ opacity: 0 }}
            animate={{ opacity: drawn ? 1 : 0 }}
            transition={{ duration: 1.5, delay: 0.5 }}
          />

          {/* ROC Curve */}
          <motion.path
            d={pathData}
            fill="none"
            stroke="#00d4ff"
            strokeWidth="3"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: drawn ? 1 : 0 }}
            transition={{ duration: 1.5, ease: "easeOut" }}
          />
          
          {/* Interactive Threshold Dot */}
          <circle cx={px} cy={py} r="6" fill="#ff3366" stroke="#0a0a0f" strokeWidth="2" />
          
          {/* Labels */}
          <text x="150" y="330" fill="rgba(255,255,255,0.5)" fontSize="12" textAnchor="middle">False Positive Rate</text>
          <text x="-150" y="-30" fill="rgba(255,255,255,0.5)" fontSize="12" textAnchor="middle" transform="rotate(-90)">True Positive Rate</text>
        </svg>
      </div>
      <div className="mt-4">
        <div className="flex justify-between text-xs text-slate-400 mb-1">
          <span>Threshold: {threshold.toFixed(2)}</span>
          <span>TPR: {((300-py)/300).toFixed(2)} | FPR: {(px/300).toFixed(2)}</span>
        </div>
        <input 
          type="range" 
          min="0" max="1" step="0.01" 
          value={threshold} 
          onChange={(e) => setThreshold(parseFloat(e.target.value))}
          className="w-full accent-primary" 
        />
      </div>
    </GlassCard>
  );
};

export default ROCCurveAnimated;
