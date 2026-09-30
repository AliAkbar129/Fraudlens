import React from 'react';
import { cn } from '@/lib/utils';
import { motion, type HTMLMotionProps } from 'framer-motion';

interface GlassCardProps {
  hoverable?: boolean;
  glowing?: boolean;
  className?: string;
  children?: React.ReactNode;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  className,
  children,
  hoverable = false,
  glowing = false,
}) => {
  return (
    <motion.div
      whileHover={hoverable ? { scale: 1.01, translateY: -2 } : {}}
      className={cn(
        'glass-card p-6 relative overflow-hidden group',
        glowing && 'before:absolute before:inset-0 before:bg-primary/5 before:opacity-0 hover:before:opacity-100 before:transition-opacity',
        className
      )}
    >
      {children}
    </motion.div>
  );
};

export default GlassCard;
