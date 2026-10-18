import torch
from torch_geometric.explain import Explainer, GNNExplainer
from torch_geometric.data import HeteroData
from loguru import logger
import json

class TargetOutput(torch.nn.Module):
    def __init__(self, model, node_type='transaction'):
        super().__init__()
        self.model = model
        self.node_type = node_type

    def forward(self, x_dict, edge_index_dict):
        return self.model(x_dict, edge_index_dict)[self.node_type]

class GNNExplainerWrapper:
    """Wrapper for PyG's GNNExplainer for heterogeneous graphs."""
    
    def __init__(self, gnn_model: torch.nn.Module, epochs: int = 100):
        self.model = gnn_model
        # Use simple Explainer setup compatible with PyG 2.3+
        self.explainer = Explainer(
            model=TargetOutput(self.model),
            algorithm=GNNExplainer(epochs=epochs),
            explanation_type='model',
            node_mask_type='attributes',
            edge_mask_type='object',
            model_config=dict(
                mode='binary_classification',
                task_level='node',
                return_type='raw',
            ),
        )

    def explain_node(self, data: HeteroData, node_idx: int, target_node_type: str = 'transaction') -> dict:
        """Generates explanation for a specific node."""
        logger.info(f"Explaining node {node_idx} of type {target_node_type}...")
        
        # Heterogeneous explaination requires targeting a specific node dictionary
        # Note: Explainer API in PyG is complex for HeteroData, this provides a structural skeleton
        self.explainer.model.node_type = target_node_type
        try:
            explanation = self.explainer(
                data.x_dict, 
                data.edge_index_dict, 
                index=node_idx
            )
            return {
                "node_mask": explanation.node_mask_dict if hasattr(explanation, 'node_mask_dict') else {},
                "edge_mask": explanation.edge_mask_dict if hasattr(explanation, 'edge_mask_dict') else {}
            }
        except Exception as e:
            raise RuntimeError("Graph explanation failed; no substitute explanation is returned") from e

    def extract_fraud_subgraph(self, explanation: dict, threshold: float = 0.5) -> list:
        """Extracts the critical subgraph."""
        edges = []
        edge_masks = explanation.get("edge_mask", {})
        for edge_type, mask in edge_masks.items():
            if mask is None: continue
            
            # mask is tensor of shape (E,)
            important_indices = (mask > threshold).nonzero(as_tuple=True)[0]
            for idx in important_indices:
                edges.append({
                    "edge_type": str(edge_type),
                    "weight": float(mask[idx])
                })
        return edges

    def to_json(self, explanation: dict) -> str:
        """Serializes to JSON."""
        # Convert tensors to lists before json dumping
        clean_exp = {"edges": self.extract_fraud_subgraph(explanation)}
        return json.dumps(clean_exp)
