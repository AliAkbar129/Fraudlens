import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/ui/GlassCard';
import DataTable from '../components/ui/DataTable';
import StatusBadge from '../components/ui/StatusBadge';
import { formatCurrency } from '@/lib/utils';
import { AlertCircle, ArrowRight } from 'lucide-react';

const CaseManagement: React.FC = () => {
  const mockCases = [
    { id: 'CAS-10492', txRef: 'TRX-99812', amount: 12500, risk: 0.94, priority: 'critical', status: 'open', analyst: 'Unassigned' },
    { id: 'CAS-10493', txRef: 'TRX-44211', amount: 450, risk: 0.82, priority: 'high', status: 'under_review', analyst: 'A. Analyst' },
    { id: 'CAS-10494', txRef: 'TRX-11234', amount: 89, risk: 0.65, priority: 'medium', status: 'resolved_fraud', analyst: 'J. Doe' },
  ];

  const columns = [
    { key: 'id', header: 'Case ID', sortable: true },
    { key: 'txRef', header: 'Transaction', sortable: true },
    { key: 'amount', header: 'Amount', sortable: true, render: (r: any) => fontMono(formatCurrency(r.amount)) },
    { key: 'risk', header: 'Risk', sortable: true, render: (r: any) => fontMono((r.risk*100).toFixed(0)+'%') },
    { key: 'priority', header: 'Priority', render: (r: any) => <StatusBadge type="priority" value={r.priority} /> },
    { key: 'status', header: 'Status', render: (r: any) => <StatusBadge type="status" value={r.status} /> },
    { key: 'analyst', header: 'Assigned To' },
  ];

  const fontMono = (text: string) => <span className="font-mono">{text}</span>;

  return (
    <div className="h-full flex gap-6">
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="flex-1 flex flex-col min-h-0"
      >
        <div className="mb-6 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Case Management</h1>
            <p className="text-slate-400">Review, investigate, and resolve flagged transactions.</p>
          </div>
          <button className="px-4 py-2 bg-primary text-black font-semibold rounded-lg hover:bg-primary/90 transition-colors">
            Auto-Assign Next
          </button>
        </div>
        
        <div className="flex-1 min-h-0">
          <DataTable data={mockCases} columns={columns} itemsPerPage={15} onRowClick={() => {}} />
        </div>
      </motion.div>

      {/* Case Detail Placeholder Panel */}
      <motion.div 
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="w-96 flex flex-col gap-4"
      >
        <GlassCard className="flex-1 flex flex-col items-center justify-center text-center p-8 text-slate-400">
          <AlertCircle className="w-12 h-12 mb-4 text-slate-500 opacity-50" />
          <h3 className="text-lg font-medium text-white mb-2">No Case Selected</h3>
          <p className="text-sm">Select a case from the queue to view details, explainability metrics, and take action.</p>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default CaseManagement;
