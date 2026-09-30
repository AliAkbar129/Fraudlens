import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ReferenceLine } from 'recharts';
import GlassCard from '../ui/GlassCard';

const mockData = Array.from({ length: 50 }).map((_, i) => ({
  latency: i * 2,
  count: Math.exp(-Math.pow(i - 15, 2) / 100) * 1000 + Math.random() * 50,
}));

export const LatencyDistribution: React.FC = () => {
  return (
    <GlassCard className="h-full w-full p-6">
      <h3 className="font-semibold text-lg mb-6 text-white">Scoring Latency Distribution</h3>
      <ResponsiveContainer width="100%" height="80%">
        <AreaChart data={mockData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#00ff88" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#00ff88" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
          <XAxis dataKey="latency" stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} unit="ms" />
          <YAxis stroke="rgba(255,255,255,0.4)" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: 'rgba(10, 10, 15, 0.9)', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
            itemStyle={{ color: '#00ff88' }}
          />
          <ReferenceLine x={30} stroke="#00d4ff" strokeDasharray="3 3" label={{ position: 'top', value: 'p50', fill: '#00d4ff', fontSize: 10 }} />
          <ReferenceLine x={60} stroke="#ffaa00" strokeDasharray="3 3" label={{ position: 'top', value: 'p95', fill: '#ffaa00', fontSize: 10 }} />
          <ReferenceLine x={80} stroke="#ff3366" strokeDasharray="3 3" label={{ position: 'top', value: 'p99', fill: '#ff3366', fontSize: 10 }} />
          <Area type="monotone" dataKey="count" stroke="#00ff88" fillOpacity={1} fill="url(#colorCount)" />
        </AreaChart>
      </ResponsiveContainer>
    </GlassCard>
  );
};

export default LatencyDistribution;
