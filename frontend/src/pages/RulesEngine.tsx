import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/ui/GlassCard';
import { ShieldAlert, Plus, Play } from 'lucide-react';
import DataTable from '../components/ui/DataTable';

const RulesEngine: React.FC = () => {
  const mockRules = [
    { id: 'RUL-001', name: 'High Velocity Transfers', action: 'auto_block', priority: 1, active: true, hits: 1420 },
    { id: 'RUL-002', name: 'New Device + Large Amount', action: 'escalate', priority: 2, active: true, hits: 843 },
    { id: 'RUL-003', name: 'Off-hours International', action: 'notify', priority: 3, active: false, hits: 0 },
  ];

  const columns = [
    { key: 'id', header: 'Rule ID' },
    { key: 'name', header: 'Rule Name' },
    { key: 'action', header: 'Action', render: (r: any) => <span className="uppercase text-xs font-bold tracking-wider">{r.action}</span> },
    { key: 'hits', header: 'Hits (30d)' },
    { key: 'active', header: 'Status', render: (r: any) => (
      <div className={`w-3 h-3 rounded-full ${r.active ? 'bg-success' : 'bg-slate-600'}`} />
    )}
  ];

  return (
    <div className="h-full flex gap-6">
      <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="flex-1 flex flex-col min-h-0">
        <div className="mb-6 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Rules Engine</h1>
            <p className="text-slate-400">Define deterministic policies that run before the ML pipeline.</p>
          </div>
          <button className="px-4 py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2">
            <Plus className="w-4 h-4" /> New Rule
          </button>
        </div>
        
        <div className="flex-1 min-h-0">
          <DataTable data={mockRules} columns={columns} />
        </div>
      </motion.div>

      <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="w-96 flex flex-col gap-4">
        <GlassCard className="flex-1 flex flex-col p-6">
          <div className="flex items-center gap-2 mb-4">
            <ShieldAlert className="w-5 h-5 text-primary" />
            <h3 className="font-semibold text-lg text-white">Rule Simulator</h3>
          </div>
          <p className="text-sm text-slate-400 mb-6">Test your rules against historical data to evaluate impact before deploying.</p>
          
          <div className="space-y-4 mb-6">
            <div>
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 block">Select Rule</label>
              <select className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white outline-none">
                <option>High Velocity Transfers</option>
                <option>New Device + Large Amount</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 block">Timeframe</label>
              <select className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white outline-none">
                <option>Last 7 Days</option>
                <option>Last 30 Days</option>
              </select>
            </div>
          </div>
          
          <button className="w-full py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg font-semibold transition-colors flex items-center justify-center gap-2 mt-auto">
            <Play className="w-4 h-4" /> Run Simulation
          </button>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default RulesEngine;
