import React from 'react';
import { Search } from 'lucide-react';

export const CommandPalette: React.FC = () => {
  return <div className='fixed inset-0 bg-black/50 z-50 flex justify-center pt-20'><div className='bg-background w-96 rounded-xl p-4'><Search /> Command Palette</div></div>;
};
export default CommandPalette;