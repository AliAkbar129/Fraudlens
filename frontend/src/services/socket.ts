import { io, Socket } from 'socket.io-client';
import { useDashboardStore } from '../stores/dashboardStore';

let socket: Socket | null = null;

export const connectSocket = () => {
  if (socket) return;
  
  socket = io(import.meta.env.VITE_WS_URL || 'http://localhost:3001', {
    autoConnect: true,
    reconnection: true,
  });

  socket.on('connect', () => {
    useDashboardStore.getState().setConnected(true);
  });

  socket.on('disconnect', () => {
    useDashboardStore.getState().setConnected(false);
  });

  socket.on('transaction_scored', (tx) => {
    useDashboardStore.getState().addTransaction(tx);
    // Auto-update dashboard metrics smoothly
  });

  socket.on('case_flagged', (alert) => {
    useDashboardStore.getState().addAlert(alert);
  });
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const getSocket = () => socket;
