from ml_pipeline.explainability.shap_explainer import SHAPExplainer
from ml_pipeline.explainability.gnn_explainer import GNNExplainerWrapper
import pandas as pd
from loguru import logger

class UnifiedExplainer:
    """Combines SHAP and GNN explanations into a unified payload."""
    
    def __init__(self, shap_explainer: SHAPExplainer, gnn_explainer: GNNExplainerWrapper):
        self.shap_explainer = shap_explainer
        self.gnn_explainer = gnn_explainer

    def explain_transaction(self, transaction_id: str, features_dict: dict, graph_data, node_idx: int, risk_score: float) -> dict:
        """Generates unified explanation."""
        logger.info(f"Generating unified explanation for {transaction_id}")
        
        # 1. SHAP (Tabular)
        tabular_exp = self.shap_explainer.explain_single(features_dict)
        
        # 2. GNN (Graph)
        gnn_raw = self.gnn_explainer.explain_node(graph_data, node_idx)
        critical_edges = self.gnn_explainer.extract_fraud_subgraph(gnn_raw)
        
        graph_exp = {
            "critical_edges": critical_edges,
            "important_nodes": [],
            "fraud_ring_size": len(critical_edges)
        }
        
        # 3. Summary
        top_feat = tabular_exp["top_features"][0]["name"] if tabular_exp["top_features"] else "Unknown"
        summary = f"Transaction {transaction_id} has a risk score of {risk_score:.2f}. " \
                  f"The most critical factor was {top_feat}. " \
                  f"It is connected to {len(critical_edges)} high-risk network entities."
                  
        return {
            "transaction_id": transaction_id,
            "risk_score": risk_score,
            "tabular_explanation": tabular_exp,
            "graph_explanation": graph_exp,
            "summary": summary
        }
