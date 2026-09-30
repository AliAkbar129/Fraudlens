export interface Transaction {
  id: number; transaction_ref: string; amount: number; currency: string;
  type: 'purchase' | 'transfer' | 'withdrawal' | 'deposit' | 'bill_payment' | 'top_up';
  channel: 'web' | 'mobile_app' | 'pos' | 'atm' | 'agent';
  sender_account?: string; receiver_account?: string; merchant_category?: string;
  device_info?: string; ip_address?: string; email?: string;
  occurred_at: string; created_at: string;
}

export interface MlScore {
  id: number; transaction_id: number; risk_score: number;
  gnn_score: number; lgbm_score: number; ensemble_method: string;
  model_version: string; latency_ms: number; is_fraud_predicted: boolean;
  confidence: number; scored_at: string;
  shap_explanation: ShapExplanation; gnn_explanation: GnnExplanation;
}

export interface ShapExplanation {
  base_value: number;
  features: Array<{ name: string; value: number; shap_value: number; direction: 'increases' | 'decreases'; description: string }>;
}

export interface GnnExplanation {
  critical_edges: Array<{ source: string; target: string; weight: number; type: string }>;
  important_nodes: Array<{ id: string; type: string; risk_score: number }>;
  fraud_ring_size: number;
}

export interface FraudCase {
  id: number; transaction_id: number; case_number: string;
  status: 'open' | 'assigned' | 'under_review' | 'escalated' | 'resolved_fraud' | 'resolved_legitimate' | 'closed';
  priority: 'critical' | 'high' | 'medium' | 'low';
  assigned_analyst?: Analyst; analyst_notes?: string;
  resolution?: string; resolution_reason?: string;
  sla_deadline?: string; resolved_at?: string; created_at: string;
  transaction?: Transaction; ml_score?: MlScore;
}

export interface Analyst { id: number; name: string; email: string; role: string; open_cases_count: number; }

export interface Rule {
  id: number; name: string; description: string;
  conditions: Array<{ field: string; operator: string; value: string | number }>;
  action: string; priority: number; is_active: boolean;
  hit_count: number; last_triggered_at?: string;
}

export interface DashboardStats {
  total_transactions_today: number; fraud_rate: number; avg_risk_score: number;
  open_cases: number; avg_latency_ms: number; model_accuracy: number;
  transactions_per_second: number; blocked_today: number;
}

export interface GraphNode {
  id: string; type: 'transaction' | 'card' | 'device' | 'ip' | 'email';
  risk_score: number; label: string; x?: number; y?: number; z?: number;
}

export interface GraphEdge {
  source: string; target: string; type: string; weight: number;
}

export interface ModelMetrics {
  precision: number; recall: number; f1: number;
  auc_pr: number; auc_roc: number; timestamp: string; model_version: string;
}

export interface AuditLogEntry { id: number; action: string; analyst: string; changes: any; created_at: string; }
