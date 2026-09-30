import React from 'react';
import { ResponsiveContainer, ComposedChart, Area, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import GlassCard from '../ui/GlassCard';

const mockData = Array.from({ length: 30 }).map((_, i) => {
  const base = 100 + Math.sin(i / 3) * 50;
  return {
    date: `Day ${i + 1}`,
    count: Math.round(base + Math.random() * 20),
    rate: (base / 10000 + Math.random() * 0.005) * 100, // percentage
  };
});

export const FraudTrendAnalysis: React.FC = () => {
  return (
    <GlassCard className="h-full w-full p-6">
      <h3 className="font-semibold text-lg mb-6 text-white">Fraud Trend Analysis (30d)</h3>
      <ResponsiveContainer width="100%" height="85%">
        <ComposedChart data={mockData} margin={{ top: 5, right: 0, bottom: 5, left: 0 }}>
          <defs>
            <linearGradient id="colorCountTrend" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ff3366" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#ff3366" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
          <XAxis dataKey="date" stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis yAxisId="left" stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis yAxisId="right" orientation="right" stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} unit="%" />
          <Tooltip 
            contentStyle={{ backgroundColor: 'rgba(10, 10, 15, 0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
          <Area yAxisId="left" type="monotone" dataKey="count" name="Fraud Count" stroke="#ff3366" fill="url(#colorCountTrend)" strokeWidth={2} />
          <Line yAxisId="right" type="monotone" dataKey="rate" name="Fraud Rate" stroke="#ffaa00" strokeWidth={2} dot={false} />
        </ComposedChart>
      </ResponsiveContainer>
    </GlassCard>
  );
};

export default FraudTrendAnalysis;
