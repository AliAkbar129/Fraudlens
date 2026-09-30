import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency: string = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount);
}

export function formatNumber(num: number) {
  return new Intl.NumberFormat('en-US').format(num);
}

export function formatDate(dateString: string) {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  }).format(date);
}

export function formatLatency(ms: number) {
  return `${ms.toFixed(1)}ms`;
}

export function getRiskColor(score: number) {
  if (score >= 0.8) return '#ff3366'; // Danger
  if (score >= 0.4) return '#ffaa00'; // Warning
  return '#00ff88'; // Success
}

export function getPriorityColor(priority: string) {
  switch (priority) {
    case 'critical': return 'text-[#ff3366] bg-[#ff3366]/10 border-[#ff3366]/20';
    case 'high': return 'text-[#ffaa00] bg-[#ffaa00]/10 border-[#ffaa00]/20';
    case 'medium': return 'text-[#00d4ff] bg-[#00d4ff]/10 border-[#00d4ff]/20';
    default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
  }
}

export function getStatusColor(status: string) {
  switch (status) {
    case 'open': return 'text-[#ff3366] bg-[#ff3366]/10 border-[#ff3366]/20';
    case 'under_review': return 'text-[#ffaa00] bg-[#ffaa00]/10 border-[#ffaa00]/20';
    case 'resolved_fraud': return 'text-[#ff3366] bg-[#ff3366]/10 border-[#ff3366]/20';
    case 'resolved_legitimate': return 'text-[#00ff88] bg-[#00ff88]/10 border-[#00ff88]/20';
    default: return 'text-slate-400 bg-slate-400/10 border-slate-400/20';
  }
}

export function truncate(str: string, length: number) {
  if (str.length <= length) return str;
  return str.slice(0, length) + '...';
}
