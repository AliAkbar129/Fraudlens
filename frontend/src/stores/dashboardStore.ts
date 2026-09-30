import { create } from 'zustand';
import { DashboardStats, Transaction, FraudCase } from '../types';

interface DashboardState {
  stats: DashboardStats;
  liveTransactions: Transaction[];
  alerts: FraudCase[];
  isConnected: boolean;
  setStats: (stats: DashboardStats) => void;
  addTransaction: (transaction: Transaction) => void;
  addAlert: (alert: FraudCase) => void;
  dismissAlert: (id: number) => void;
  setConnected: (status: boolean) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  stats: {
    total_transactions_today: 124500,
    fraud_rate: 0.045,
    avg_risk_score: 0.12,
    open_cases: 342,
    avg_latency_ms: 45,
    model_accuracy: 99.1,
    transactions_per_second: 340,
    blocked_today: 1205
  },
  liveTransactions: [],
  alerts: [],
  isConnected: false,
  setStats: (stats) => set({ stats }),
  addTransaction: (transaction) => set((state) => ({
    liveTransactions: [transaction, ...state.liveTransactions].slice(0, 100)
  })),
  addAlert: (alert) => set((state) => ({
    alerts: [alert, ...state.alerts].slice(0, 50)
  })),
  dismissAlert: (id) => set((state) => ({
    alerts: state.alerts.filter(a => a.id !== id)
  })),
  setConnected: (isConnected) => set({ isConnected }),
}));
