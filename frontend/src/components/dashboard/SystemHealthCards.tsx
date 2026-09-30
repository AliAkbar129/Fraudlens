import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../ui/GlassCard';
import { Server, Database, Wifi } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer } from 'recharts';

const mockData = Array.from({ length: 20 }).map(() => ({ value: Math.random() * 10 + 90 }));

export const SystemHealthCards: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <GlassCard className="p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-primary/10 rounded-xl">
            <Server className="w-6 h-6 text-primary" />
          </div>
          <div>
            <div className="text-sm text-slate-400 font-medium">ML Inference Engine</div>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse-glow" />
              <span className="text-white font-semibold">Online (99.9%)</span>
            </div>
          </div>
        </div>
        <div className="w-24 h-12">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockData}>
              <Line type="monotone" dataKey="value" stroke="#00d4ff" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>

      <GlassCard className="p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-success/10 rounded-xl">
            <Database className="w-6 h-6 text-success" />
          </div>
          <div>
            <div className="text-sm text-slate-400 font-medium">Graph Database</div>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse-glow" />
              <span className="text-white font-semibold">Online (4ms)</span>
            </div>
          </div>
        </div>
        <div className="w-24 h-12">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockData}>
              <Line type="monotone" dataKey="value" stroke="#00ff88" strokeWidth={2} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>

      <GlassCard className="p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-warning/10 rounded-xl">
            <Wifi className="w-6 h-6 text-warning" />
          </div>
          <div>
            <div className="text-sm text-slate-400 font-medium">Event Stream</div>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 rounded-full bg-success animate-pulse-glow" />
              <span className="text-white font-semibold">Connected</span>
            </div>
          </div>
        </div>
        <div className="text-right">
          <div className="text-lg font-mono font-bold text-white">4,291</div>
          <div className="text-xs text-slate-400">msg/sec</div>
        </div>
      </GlassCard>
    </div>
  );
};

export default SystemHealthCards;
