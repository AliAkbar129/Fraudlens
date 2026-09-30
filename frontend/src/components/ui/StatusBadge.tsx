import React from 'react';
import { cn, getPriorityColor, getStatusColor } from '@/lib/utils';
import { motion } from 'framer-motion';

interface StatusBadgeProps {
  type: 'status' | 'priority';
  value: string;
  className?: string;
  showDot?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  type,
  value,
  className,
  showDot = true,
}) => {
  const colorClass = type === 'priority' ? getPriorityColor(value) : getStatusColor(value);
  const formattedValue = value.replace(/_/g, ' ').toUpperCase();

  return (
    <div className={cn(
      "inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wider border",
      colorClass,
      className
    )}>
      {showDot && (
        <motion.div 
          animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }} 
          transition={{ repeat: Infinity, duration: 2 }}
          className="w-1.5 h-1.5 rounded-full bg-current" 
        />
      )}
      {formattedValue}
    </div>
  );
};

export default StatusBadge;
