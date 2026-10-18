import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, GATConv, to_hetero, Linear
from torch_geometric.data import HeteroData

class GraphSAGEModel(torch.nn.Module):
    """Homogeneous GraphSAGE."""
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=2, dropout=0.3):
        super().__init__()
        self.dropout = torch.nn.Dropout(dropout)
        self.convs = torch.nn.ModuleList()
        self.convs.append(SAGEConv(in_channels, hidden_channels))
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_channels, hidden_channels))
        self.convs.append(SAGEConv(hidden_channels, out_channels))

    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs[:-1]):
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        x = self.convs[-1](x, edge_index)
        return x

class GATModel(torch.nn.Module):
    """Homogeneous GAT."""
    def __init__(self, in_channels, hidden_channels, out_channels, num_layers=2, heads=4, dropout=0.3):
        super().__init__()
        self.dropout = torch.nn.Dropout(dropout)
        self.convs = torch.nn.ModuleList()
        self.convs.append(GATConv(in_channels, hidden_channels, heads=heads, add_self_loops=False))
        for _ in range(num_layers - 2):
            self.convs.append(GATConv(hidden_channels * heads, hidden_channels, heads=heads, add_self_loops=False))
        self.convs.append(GATConv(hidden_channels * heads, out_channels, heads=1, concat=False, add_self_loops=False))

    def forward(self, x, edge_index):
        for i, conv in enumerate(self.convs[:-1]):
            x = conv(x, edge_index)
            x = F.relu(x)
            x = self.dropout(x)
        x = self.convs[-1](x, edge_index)
        return x

class HeteroGNN(torch.nn.Module):
    """Heterogeneous GNN Wrapper."""
    def __init__(self, hidden_channels, out_channels, metadata, base_model="graphsage", num_layers=2, dropout=0.3, heads=4):
        super().__init__()
        # Initial projection for each node type to match hidden dimensions
        self.lin_dict = torch.nn.ModuleDict()
        for node_type in metadata[0]:
            self.lin_dict[node_type] = Linear(-1, hidden_channels)
            
        if base_model.lower() == "graphsage":
            model = GraphSAGEModel(hidden_channels, hidden_channels, out_channels, num_layers, dropout)
        elif base_model.lower() == "gat":
            model = GATModel(hidden_channels, hidden_channels, out_channels, num_layers, heads, dropout)
        else:
            raise ValueError(f"Unknown base model: {base_model}")
            
        self.gnn = to_hetero(model, metadata, aggr='sum')

    def forward(self, x_dict, edge_index_dict):
        # Project inputs
        h_dict = {node_type: self.lin_dict[node_type](x) for node_type, x in x_dict.items()}
        # Apply HeteroGNN
        out_dict = self.gnn(h_dict, edge_index_dict)
        return out_dict
