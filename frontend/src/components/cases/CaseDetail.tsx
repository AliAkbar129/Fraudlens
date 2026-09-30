import React from 'react';
import GlassCard from '../ui/GlassCard';
import RiskGauge from '../ui/RiskGauge';

export const CaseDetail: React.FC = () => {
  return <GlassCard><RiskGauge score={0.9} /><div>Case Detail</div></GlassCard>;
};
export default CaseDetail;