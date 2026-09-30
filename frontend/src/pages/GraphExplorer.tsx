import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/ui/GlassCard';
import ForceGraph3D from '../components/3d/ForceGraph3D';
import { Filter, SlidersHorizontal, Layers, Play } from 'lucide-react';

const GraphExplorer = () => {
  return (
    <div className="h-full flex flex-col">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Graph Explorer</h1>
        <p className="text-slate-400">Investigate fraud rings and complex network relationships in 3D.</p>
      </motion.div>

      <div className="flex-1 flex gap-6 min-h-0">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="w-80 flex flex-col gap-4"
        >
          <GlassCard className="flex-1 overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-lg flex items-center gap-2">
                <Filter className="w-4 h-4 text-primary" /> Filters
              </h3>
            </div>
            
            <div className="space-y-6">
              <div>
                <label className="text-sm font-medium text-slate-300 mb-2 block">Risk Threshold</label>
                <input type="range" className="w-full accent-primary" min="0" max="100" defaultValue="75" />
                <div className="flex justify-between text-xs text-slate-500 mt-1">
                  <span>Safe (0.0)</span>
                  <span>Critical (1.0)</span>
                </div>
              </div>
              
              <div className="h-px bg-white/10" />
              
              <div>
                <label className="text-sm font-medium text-slate-300 mb-3 block flex items-center gap-2">
                  <Layers className="w-4 h-4 text-slate-400" /> Entity Types
                </label>
                <div className="space-y-2">
                  {['Transactions', 'Credit Cards', 'Devices', 'IP Addresses', 'Emails'].map((label, i) => (
                    <label key={i} className="flex items-center gap-3 cursor-pointer group">
                      <div className="w-4 h-4 rounded border border-white/20 bg-black/20 flex items-center justify-center group-hover:border-primary/50">
                        <div className="w-2 h-2 bg-primary rounded-sm" />
                      </div>
                      <span className="text-sm text-slate-300 group-hover:text-white transition-colors">{label}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>
          </GlassCard>
          
          <GlassCard className="h-48">
            <h3 className="font-semibold text-sm text-slate-300 mb-4 flex items-center gap-2">
              <SlidersHorizontal className="w-4 h-4 text-primary" /> Simulation Controls
            </h3>
            <div className="space-y-3">
              <button className="w-full py-2 bg-primary/10 hover:bg-primary/20 text-primary rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2">
                <Play className="w-4 h-4" /> Resume Physics
              </button>
            </div>
          </GlassCard>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="flex-1"
        >
          <ForceGraph3D />
        </motion.div>
      </div>
    </div>
  );
};

export default GraphExplorer;
