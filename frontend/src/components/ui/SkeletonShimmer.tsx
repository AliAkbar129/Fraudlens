import React from 'react';
import { cn } from '@/lib/utils';

interface SkeletonShimmerProps {
  className?: string;
}

export const SkeletonShimmer: React.FC<SkeletonShimmerProps> = ({ className }) => {
  return (
    <div 
      className={cn(
        "relative overflow-hidden bg-white/5 rounded-md before:absolute before:inset-0 before:-translate-x-full before:animate-shimmer before:bg-gradient-to-r before:from-transparent before:via-white/10 before:to-transparent",
        className
      )}
    />
  );
};

export default SkeletonShimmer;
