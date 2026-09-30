import React from 'react';
import { motion } from 'framer-motion';
import ModelPerformance from '../components/charts/ModelPerformance';
import LatencyDistribution from '../components/charts/LatencyDistribution';
import ROCCurveAnimated from '../components/charts/ROCCurveAnimated';
import FraudTrendAnalysis from '../components/charts/FraudTrendAnalysis';
import PrecisionRecallTradeoff from '../components/charts/PrecisionRecallTradeoff';
import GlassCard from '../components/ui/GlassCard';

const Analytics: React.FC = () => {
  return (
    <div className="h-full flex flex-col overflow-y-auto pr-2 pb-10">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Analytics & Models</h1>
        <p className="text-slate-400">Deep dive into model performance, latency distributions, and macro fraud trends.</p>
      </motion.div>

      <div className="flex flex-col gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <ModelPerformance />
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <LatencyDistribution />
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
            <ROCCurveAnimated />
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
            <FraudTrendAnalysis />
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
            <PrecisionRecallTradeoff />
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
