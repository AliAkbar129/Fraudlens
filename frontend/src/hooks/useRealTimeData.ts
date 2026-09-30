import { useEffect } from 'react';
import { connectSocket, disconnectSocket } from '../services/socket';

export const useRealTimeData = () => {
  useEffect(() => {
    connectSocket();
    return () => {
      disconnectSocket();
    };
  }, []);
};
