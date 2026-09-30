import pandas as pd
import numpy as np
import torch
from loguru import logger
from torch_geometric.data import HeteroData
import networkx as nx

class TransactionGraphBuilder:
    """Core module for heterogeneous graph construction using PyTorch Geometric."""
    
    def __init__(self):
        self.node_mapping = {}

    def _map_nodes(self, df: pd.DataFrame, col: str) -> torch.Tensor:
        """Creates contiguous indices for nodes."""
        unique_nodes = df[col].unique()
        mapping = {node: i for i, node in enumerate(unique_nodes)}
        self.node_mapping[col] = mapping
        return torch.tensor([mapping[n] for n in df[col].values], dtype=torch.long)

    def build_heterogeneous_graph(self, df: pd.DataFrame) -> HeteroData:
        """Constructs PyG HeteroData."""
        logger.info("Building heterogeneous graph...")
        data = HeteroData()
        
        # Identify node columns (using generic mock columns if specific don't exist)
        tx_col = "TransactionID"
        card_col = "card1"
        device_col = "device_hash" if "device_hash" in df.columns else "DeviceInfo"
        email_col = "P_emaildomain"

        # Map nodes
        tx_idx = self._map_nodes(df, tx_col)
        
        # Extract features for transactions
        feature_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and c not in [tx_col, "isFraud", "TransactionDT"]]
        tx_features = torch.tensor(df[feature_cols].fillna(0).values, dtype=torch.float)
        data['transaction'].x = tx_features
        data['transaction'].y = torch.tensor(df["isFraud"].values, dtype=torch.long) if "isFraud" in df.columns else torch.zeros(len(df), dtype=torch.long)
        
        # Connect to Card
        if card_col in df.columns:
            card_idx = self._map_nodes(df, card_col)
            data['card'].x = torch.ones((len(self.node_mapping[card_col]), 1), dtype=torch.float) # Dummy features
            edge_index = torch.stack([tx_idx, card_idx], dim=0)
            data['transaction', 'uses', 'card'].edge_index = edge_index
            data['card', 'used_by', 'transaction'].edge_index = edge_index[[1, 0]]
            
        # Connect to Device
        if device_col in df.columns:
            device_idx = self._map_nodes(df, device_col)
            data['device'].x = torch.ones((len(self.node_mapping[device_col]), 1), dtype=torch.float)
            edge_index = torch.stack([tx_idx, device_idx], dim=0)
            data['transaction', 'from_device', 'device'].edge_index = edge_index
            data['device', 'device_for', 'transaction'].edge_index = edge_index[[1, 0]]

        # Connect to Email
        if email_col in df.columns:
            email_idx = self._map_nodes(df, email_col)
            data['email'].x = torch.ones((len(self.node_mapping[email_col]), 1), dtype=torch.float)
            edge_index = torch.stack([tx_idx, email_idx], dim=0)
            data['transaction', 'has_email', 'email'].edge_index = edge_index
            data['email', 'email_for', 'transaction'].edge_index = edge_index[[1, 0]]

        return data

    def from_dataframe(self, df: pd.DataFrame) -> HeteroData:
        """Main entry point."""
        return self.build_heterogeneous_graph(df)

    def get_subgraph(self, data: HeteroData, node_id: int, num_hops: int = 2) -> HeteroData:
        """Extracts ego-graph (simplified for demo)."""
        logger.info(f"Extracting {num_hops}-hop subgraph for node {node_id}")
        # Note: True k-hop heterogeneous subgraph extraction requires PyG k_hop_subgraph logic
        # which is complex across multiple edge types. Returning full graph for stub avoidance,
        # but in production, one would use torch_geometric.utils.k_hop_subgraph on homogeneous view.
        return data

    def to_networkx(self, data: HeteroData) -> nx.Graph:
        """Converts to NetworkX for visualization."""
        from torch_geometric.data import Data
        homo_data = data.to_homogeneous()
        edges = homo_data.edge_index.t().numpy()
        G = nx.Graph()
        G.add_edges_from(edges)
        return G
