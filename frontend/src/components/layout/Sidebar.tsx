import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Network, Briefcase, BarChart3, ShieldAlert, Settings, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

const navItems = [
  { icon: LayoutDashboard, label: 'Command Center', path: '/command-center' },
  { icon: Network, label: 'Graph Explorer', path: '/graph-explorer' },
  { icon: Briefcase, label: 'Cases', path: '/cases' },
  { icon: BarChart3, label: 'Analytics', path: '/analytics' },
  { icon: ShieldAlert, label: 'Rules Engine', path: '/rules' },
  { icon: Settings, label: 'Settings', path: '/settings' },
];

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 border-r border-white/10 bg-black/40 backdrop-blur-xl flex flex-col z-20 shrink-0">
      <div className="h-16 flex items-center px-6 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary flex items-center justify-center">
            <ShieldAlert className="w-5 h-5 text-primary" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white glow-text">FraudLens</span>
        </div>
      </div>

      <nav className="flex-1 py-6 px-3 flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 relative group',
                isActive ? 'text-white' : 'text-slate-400 hover:text-white hover:bg-white/5'
              )
            }
          >
            {({ isActive }) => (
              <>
                {isActive && (
                  <motion.div
                    layoutId="active-nav"
                    className="absolute inset-0 bg-primary/10 rounded-xl border border-primary/20"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
                <item.icon className="w-5 h-5 relative z-10" />
                <span className="font-medium relative z-10">{item.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-white/10">
        <div className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors cursor-pointer">
          <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-purple-500 flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1 overflow-hidden">
            <div className="font-medium text-sm text-white truncate">Alex Analyst</div>
            <div className="text-xs text-primary truncate">L3 Investigator</div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
