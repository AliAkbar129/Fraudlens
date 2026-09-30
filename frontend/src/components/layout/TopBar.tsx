import React from 'react';
import { Search, Bell } from 'lucide-react';
import { useDashboardStore } from '@/stores/dashboardStore';

const TopBar: React.FC = () => {
  const isConnected = useDashboardStore(state => state.isConnected);

  return (
    <header className="h-16 border-b border-white/10 bg-black/20 backdrop-blur-md flex items-center justify-between px-6 z-10 shrink-0">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative w-96 group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-primary transition-colors" />
          <input
            type="text"
            placeholder="Search transactions, cases, or ⌘K"
            className="w-full bg-white/5 border border-white/10 rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-primary/50 focus:bg-white/10 transition-all text-white placeholder:text-slate-500"
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex gap-1">
            <kbd className="px-1.5 py-0.5 bg-white/10 rounded text-[10px] font-mono text-slate-400">⌘</kbd>
            <kbd className="px-1.5 py-0.5 bg-white/10 rounded text-[10px] font-mono text-slate-400">K</kbd>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-6">
        <div className="flex items-center gap-2">
          <div className="relative">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success animate-pulse-glow' : 'bg-danger'}`} />
          </div>
          <span className="text-xs font-mono text-slate-400">
            {isConnected ? 'SYSTEM ONLINE' : 'DISCONNECTED'}
          </span>
        </div>

        <button className="relative p-2 rounded-full hover:bg-white/10 transition-colors text-slate-300 hover:text-white">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-danger rounded-full border border-[#0a0a0f]" />
        </button>
      </div>
    </header>
  );
};

export default TopBar;
