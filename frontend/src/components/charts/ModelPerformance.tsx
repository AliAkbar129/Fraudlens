import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import GlassCard from '../ui/GlassCard';

const mockData = Array.from({ length: 24 }).map((_, i) => ({
  time: `${i}:00`,
  precision: 0.85 + Math.random() * 0.1,
  recall: 0.80 + Math.random() * 0.15,
  f1: 0.82 + Math.random() * 0.12,
  auc: 0.92 + Math.random() * 0.05,
}));

export const ModelPerformance: React.FC = () => {
  return (
    <GlassCard className="h-[400px] w-full p-6">
      <h3 className="font-semibold text-lg mb-6 text-white">Model Performance (24h)</h3>
      <ResponsiveContainer width="100%" height="85%">
        <LineChart data={mockData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
          <XAxis dataKey="time" stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} domain={[0.6, 1]} tickLine={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'rgba(10, 10, 15, 0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px', backdropFilter: 'blur(10px)' }}
            itemStyle={{ fontSize: '14px', fontWeight: 500 }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Line type="monotone" dataKey="precision" name="Precision" stroke="#00d4ff" strokeWidth={3} dot={false} activeDot={{ r: 6, fill: '#00d4ff', stroke: '#0a0a0f', strokeWidth: 2 }} />
          <Line type="monotone" dataKey="recall" name="Recall" stroke="#00ff88" strokeWidth={3} dot={false} activeDot={{ r: 6, fill: '#00ff88', stroke: '#0a0a0f', strokeWidth: 2 }} />
          <Line type="monotone" dataKey="f1" name="F1 Score" stroke="#a855f7" strokeWidth={2} dot={false} strokeDasharray="5 5" />
          <Line type="monotone" dataKey="auc" name="AUC-PR" stroke="#ffaa00" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </GlassCard>
  );
};

export default ModelPerformance;
