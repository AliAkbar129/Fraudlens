import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, CreditCard, Laptop, ArrowRight } from 'lucide-react';
import { useDashboardStore } from '@/stores/dashboardStore';
import { formatCurrency, formatNumber } from '@/lib/utils';
import StatusBadge from '../ui/StatusBadge';

export const AlertFeed: React.FC = () => {
  const alerts = useDashboardStore(state => state.alerts);
  
  // Generating some mock alerts if empty to show the UI
  const displayAlerts = alerts.length > 0 ? alerts : [
    {
      id: 1,
      case_number: 'CAS-10492',
      status: 'open',
      priority: 'critical',
      transaction: { amount: 12500.00, currency: 'USD', type: 'transfer', transaction_ref: 'TRX-99812-A' },
      ml_score: { risk_score: 0.94 }
    },
    {
      id: 2,
      case_number: 'CAS-10493',
      status: 'open',
      priority: 'high',
      transaction: { amount: 450.00, currency: 'USD', type: 'purchase', transaction_ref: 'TRX-44211-B' },
      ml_score: { risk_score: 0.82 }
    },
    {
      id: 3,
      case_number: 'CAS-10494',
      status: 'under_review',
      priority: 'medium',
      transaction: { amount: 89.99, currency: 'USD', type: 'purchase', transaction_ref: 'TRX-11234-C' },
      ml_score: { risk_score: 0.65 }
    }
  ];

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <div className="flex-1 overflow-y-auto pr-2 space-y-3">
        <AnimatePresence initial={false}>
          {displayAlerts.slice(0, 10).map((alert: any) => (
            <motion.div
              key={alert.id}
              initial={{ opacity: 0, x: 20, scale: 0.95 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              className={`p-4 rounded-xl border-l-4 bg-white/5 border-y border-r border-y-white/5 border-r-white/5 hover:bg-white/10 cursor-pointer transition-colors group relative overflow-hidden`}
              style={{
                borderLeftColor: alert.priority === 'critical' ? '#ff3366' : alert.priority === 'high' ? '#ffaa00' : '#00d4ff'
              }}
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-2">
                  <ShieldAlert className="w-4 h-4 text-slate-400" />
                  <span className="font-mono text-sm text-white font-semibold">{alert.transaction.transaction_ref}</span>
                </div>
                <StatusBadge type="priority" value={alert.priority} />
              </div>
              
              <div className="flex justify-between items-end">
                <div>
                  <div className="text-xl font-bold text-white mb-1">
                    {formatCurrency(alert.transaction.amount, alert.transaction.currency)}
                  </div>
                  <div className="text-xs text-slate-400 flex items-center gap-2">
                    <CreditCard className="w-3 h-3" /> {alert.transaction.type.toUpperCase()}
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-bold font-mono ${alert.ml_score.risk_score >= 0.8 ? 'text-danger' : 'text-warning'}`}>
                    {(alert.ml_score.risk_score * 100).toFixed(0)}% RISK
                  </div>
                  <div className="text-xs text-slate-500">AI CONFIDENCE</div>
                </div>
              </div>

              <div className="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                  <ArrowRight className="w-4 h-4 text-white" />
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AlertFeed;
