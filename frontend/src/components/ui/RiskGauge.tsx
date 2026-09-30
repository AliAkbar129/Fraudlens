import React from 'react';
import { motion } from 'framer-motion';
import { getRiskColor } from '@/lib/utils';

interface RiskGaugeProps {
  score: number; // 0 to 1
  size?: number;
  strokeWidth?: number;
}

export const RiskGauge: React.FC<RiskGaugeProps> = ({
  score,
  size = 120,
  strokeWidth = 10,
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDashoffset = circumference - score * circumference;
  
  const color = getRiskColor(score);
  const isHighRisk = score >= 0.8;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      {isHighRisk && (
        <div 
          className="absolute inset-0 rounded-full animate-pulse-glow" 
          style={{ backgroundColor: color, filter: 'blur(20px)', opacity: 0.2 }}
        />
      )}
      <svg width={size} height={size} className="transform -rotate-90 relative z-10">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-white/10"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.span 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-2xl font-bold font-mono text-white"
        >
          {Math.round(score * 100)}
        </motion.span>
        <span className="text-[10px] text-slate-400 font-medium uppercase tracking-wider">
          Risk Score
        </span>
      </div>
    </div>
  );
};

export default RiskGauge;
