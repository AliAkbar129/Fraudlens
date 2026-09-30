import React from 'react';
import DataTable from '../ui/DataTable';

export const CaseQueue: React.FC = () => {
  return <div className='h-full'><DataTable data={[]} columns={[]} emptyMessage='Queue loaded.' /></div>;
};
export default CaseQueue;