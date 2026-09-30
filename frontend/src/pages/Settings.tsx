import React from 'react';
import { motion } from 'framer-motion';
import GlassCard from '../components/ui/GlassCard';
import { User, Bell, Key, Settings as SettingsIcon, Database } from 'lucide-react';

const Settings: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto h-full overflow-y-auto pb-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight text-white mb-1">Settings</h1>
        <p className="text-slate-400">Manage your account, preferences, and system configuration.</p>
      </motion.div>

      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <GlassCard className="p-6">
            <h3 className="font-semibold text-lg text-white mb-4 flex items-center gap-2"><User className="w-5 h-5 text-primary" /> Profile Settings</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Full Name</label>
                <input type="text" defaultValue="Alex Analyst" className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white" />
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Email</label>
                <input type="email" defaultValue="alex@fraudlens.io" className="w-full bg-white/5 border border-white/10 rounded-lg p-2 text-white" />
              </div>
            </div>
            <button className="mt-4 px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20">Save Changes</button>
          </GlassCard>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <GlassCard className="p-6">
            <h3 className="font-semibold text-lg text-white mb-4 flex items-center gap-2"><SettingsIcon className="w-5 h-5 text-primary" /> Model Configuration</h3>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Critical Priority Threshold (0-100%)</label>
                <input type="range" className="w-full accent-danger" min="0" max="100" defaultValue="85" />
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Auto-Block Threshold (0-100%)</label>
                <input type="range" className="w-full accent-primary" min="0" max="100" defaultValue="95" />
              </div>
            </div>
          </GlassCard>
        </motion.div>
      </div>
    </div>
  );
};

export default Settings;
