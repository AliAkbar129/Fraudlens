import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Info, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

export type ToastType = 'info' | 'success' | 'warning' | 'error';

interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

export const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (type: ToastType, message: string) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => {
      removeToast(id);
    }, 5000);
  };

  const removeToast = (id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  return { toasts, addToast, removeToast };
};

export const ToastContainer: React.FC<{ toasts: Toast[]; removeToast: (id: number) => void }> = ({ toasts, removeToast }) => {
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            initial={{ opacity: 0, x: 50, scale: 0.9 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
            className={cn(
              "pointer-events-auto p-4 rounded-xl backdrop-blur-xl border shadow-lg flex items-start gap-3 w-80 relative overflow-hidden",
              {
                'bg-blue-500/10 border-blue-500/20 text-blue-200': toast.type === 'info',
                'bg-emerald-500/10 border-emerald-500/20 text-emerald-200': toast.type === 'success',
                'bg-amber-500/10 border-amber-500/20 text-amber-200': toast.type === 'warning',
                'bg-rose-500/10 border-rose-500/20 text-rose-200': toast.type === 'error',
              }
            )}
          >
            <div className="mt-0.5">
              {toast.type === 'info' && <Info className="w-4 h-4 text-blue-400" />}
              {toast.type === 'success' && <CheckCircle className="w-4 h-4 text-emerald-400" />}
              {toast.type === 'warning' && <AlertTriangle className="w-4 h-4 text-amber-400" />}
              {toast.type === 'error' && <XCircle className="w-4 h-4 text-rose-400" />}
            </div>
            <div className="flex-1 text-sm font-medium">{toast.message}</div>
            <button onClick={() => removeToast(toast.id)} className="text-white/50 hover:text-white transition-colors">
              <X className="w-4 h-4" />
            </button>
            <motion.div 
              initial={{ width: "100%" }} 
              animate={{ width: "0%" }} 
              transition={{ duration: 5, ease: "linear" }}
              className={cn("absolute bottom-0 left-0 h-1", {
                'bg-blue-500': toast.type === 'info',
                'bg-emerald-500': toast.type === 'success',
                'bg-amber-500': toast.type === 'warning',
                'bg-rose-500': toast.type === 'error',
              })} 
            />
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};
