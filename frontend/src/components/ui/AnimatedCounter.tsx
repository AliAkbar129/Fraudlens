import React, { useEffect, useRef } from 'react';
import { useSpring, useTransform, motion } from 'framer-motion';

interface AnimatedCounterProps {
  value: number;
  duration?: number; // In ms
  prefix?: string;
  suffix?: string;
  decimals?: number;
  className?: string;
}

export const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  value,
  duration = 1000,
  prefix = '',
  suffix = '',
  decimals = 0,
  className = '',
}) => {
  const springValue = useSpring(0, {
    stiffness: 100,
    damping: 30,
    mass: 1,
    duration: duration,
  });

  const displayValue = useTransform(springValue, (current) => {
    return (
      prefix +
      current.toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
      }) +
      suffix
    );
  });

  useEffect(() => {
    springValue.set(value);
  }, [value, springValue]);

  return (
    <motion.span className={`font-mono ${className}`}>
      {displayValue}
    </motion.span>
  );
};

export default AnimatedCounter;
