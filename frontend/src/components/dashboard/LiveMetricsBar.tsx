import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../ui/GlassCard';
import { useDashboardStore } from '@/stores/dashboardStore';
import { useAnimatedCounter } from '@/hooks/useAnimatedCounter';
import { formatNumber, formatCurrency } from '@/lib/utils';
import { Activity, ShieldAlert, Zap, TrendingUp, AlertTriangle } from 'lucide-react';

const MetricCard = ({ title, value, icon: Icon, prefix = '', suffix = '', isCurrency = false, isPercentage = false, decimals = 0, colorClass = "text-primary" }: any) => {
  const animatedValue = useAnimatedCounter(value, 1500);
  
  const displayValue = isCurrency 
    ? formatCurrency(animatedValue) 
    : isPercentage
      ? `${animatedValue.toFixed(decimals)}%`
      : formatNumber(Math.round(animatedValue));

  return (
    <GlassCard hoverable className="p-4 flex items-center justify-between col-span-1">
      <div>
        <div className="text-slate-400 text-xs font-medium mb-1">{title}</div>
        <div className="text-2xl font-bold font-mono tracking-tight text-white flex items-baseline">
          {prefix}{displayValue}{suffix}
        </div>
      </div>
      <div className={`p-3 rounded-xl bg-white/5 ${colorClass}`}>
        <Icon className="w-5 h-5" />
      </div>
    </GlassCard>
  );
};

export const LiveMetricsBar: React.FC = () => {
  const stats = useDashboardStore(state => state.stats);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { type: 'spring', stiffness: 300, damping: 24 } }
  };

  return (
    <motion.div 
      variants={container} 
      initial="hidden" 
      animate="show" 
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6"
    >
      <motion.div variants={item} className="contents">
        <MetricCard title="Transactions / Sec" value={stats.transactions_per_second} icon={Activity} />
      </motion.div>
      <motion.div variants={item} className="contents">
        <MetricCard title="Fraud Rate (24h)" value={stats.fraud_rate * 100} isPercentage decimals={2} icon={ShieldAlert} colorClass="text-danger" />
      </motion.div>
      <motion.div variants={item} className="contents">
        <MetricCard title="Avg Score" value={stats.avg_risk_score} icon={TrendingUp} colorClass="text-warning" />
      </motion.div>
      <motion.div variants={item} className="contents">
        <MetricCard title="Open Cases" value={stats.open_cases} icon={AlertTriangle} colorClass="text-warning" />
      </motion.div>
      <motion.div variants={item} className="contents">
        <MetricCard title="Avg Latency" value={stats.avg_latency_ms} icon={Zap} suffix="ms" colorClass="text-success" />
      </motion.div>
    </motion.div>
  );
};
