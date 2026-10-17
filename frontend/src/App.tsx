import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import AppLayout from './components/layout/AppLayout';
import CommandCenter from './pages/CommandCenter';
import GraphExplorer from './pages/GraphExplorer';
import CaseManagement from './pages/CaseManagement';
import Analytics from './pages/Analytics';
import RulesEngine from './pages/RulesEngine';
import Settings from './pages/Settings';

function App() {
  return (
    <div className="min-h-screen bg-background text-text">
      <AppLayout>
        <aside role="status" className="p-3 border border-amber-500 text-amber-200">Legacy prototype: some screens contain demonstration data. For measured synthetic-data experiments, run the research_lab workbench documented in the README.</aside>
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<Navigate to="/command-center" replace />} />
            <Route path="/command-center" element={<CommandCenter />} />
            <Route path="/graph-explorer" element={<GraphExplorer />} />
            <Route path="/cases" element={<CaseManagement />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/rules" element={<RulesEngine />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </AnimatePresence>
      </AppLayout>
    </div>
  );
}

export default App;
