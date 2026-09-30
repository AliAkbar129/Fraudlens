import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/ui/GlassCard';
import { LiveMetricsBar } from '../components/dashboard/LiveMetricsBar';
import TransactionGlobe from '../components/3d/TransactionGlobe';
import AlertFeed from '../components/dashboard/AlertFeed';
import SystemHealthCards from '../components/dashboard/SystemHealthCards';
import RiskHeatmap from '../components/dashboard/RiskHeatmap';

const CommandCenter: React.FC = () => {
  return (
    <div className="h-full flex flex-col">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6 flex justify-between items-end"
      >
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Command Center</h1>
          <p className="text-slate-400">Real-time fraud detection and system monitoring overview.</p>
        </div>
      </motion.div>

      <LiveMetricsBar />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-2 h-[500px] xl:h-auto"
        >
          <GlassCard className="h-full p-0 overflow-hidden flex flex-col relative">
            <div className="absolute top-4 left-6 z-10 pointer-events-none">
              <h3 className="font-semibold text-lg">Global Transaction Flow</h3>
              <div className="text-xs text-slate-400 flex items-center gap-2 mt-1">
                <span className="w-2 h-2 rounded-full bg-primary inline-block animate-pulse-glow" /> Live Feed
              </div>
            </div>
            
            <div className="flex-1 w-full h-full">
              <TransactionGlobe />
            </div>
          </GlassCard>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="flex flex-col h-[500px] xl:h-auto"
        >
          <GlassCard className="h-full flex flex-col p-4">
            <h3 className="font-semibold text-lg mb-4 pl-2">Critical Alerts Feed</h3>
            <div className="flex-1 min-h-0">
              <AlertFeed />
            </div>
          </GlassCard>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <RiskHeatmap />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="flex flex-col justify-center"
        >
          <h3 className="font-semibold text-lg mb-4 text-white">Live System Health</h3>
          <SystemHealthCards />
        </motion.div>
      </div>
    </div>
  );
};

export default CommandCenter;
