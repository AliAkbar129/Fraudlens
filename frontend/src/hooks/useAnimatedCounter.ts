import { useState, useEffect } from 'react';

export function useAnimatedCounter(
  end: number,
  duration: number = 1000
) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const updateCounter = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;

      if (progress < duration) {
        // Easing function (easeOutExpo)
        const easeProgress = progress / duration;
        const easedProgress = easeProgress === 1 ? 1 : 1 - Math.pow(2, -10 * easeProgress);
        
        setCount(end * easedProgress);
        animationFrame = requestAnimationFrame(updateCounter);
      } else {
        setCount(end);
      }
    };

    animationFrame = requestAnimationFrame(updateCounter);

    return () => cancelAnimationFrame(animationFrame);
  }, [end, duration]);

  return count;
}
