import pytest
import pandas as pd
import numpy as np
import torch
from torch_geometric.data import HeteroData
import lightgbm as lgb

@pytest.fixture
def sample_transaction_data():
    return pd.DataFrame({
        "TransactionID": range(1, 101),
        "isFraud": [0] * 90 + [1] * 10,
        "TransactionDT": range(1000, 1100),
        "TransactionAmt": [10.5] * 100,
        "card1": [1234] * 100,
        "P_emaildomain": ["gmail.com"] * 100,
        "DeviceInfo": ["Windows"] * 100,
        "id_31": ["chrome"] * 100
    })

@pytest.fixture
def sample_graph_data():
    torch.manual_seed(42)
    data = HeteroData()
    data['transaction'].x = torch.rand(10, 5)
    data['transaction'].y = torch.randint(0, 2, (10,))
    data['card'].x = torch.rand(5, 2)
    
    # Edges
    tx_idx = torch.arange(10)
    card_idx = torch.arange(10) % 5
    edge_index = torch.stack([tx_idx, card_idx], dim=0)
    
    data['transaction', 'uses', 'card'].edge_index = edge_index
    data['card', 'used_by', 'transaction'].edge_index = edge_index[[1, 0]]
    
    return data

@pytest.fixture
def trained_lgbm_model():
    X = np.random.rand(100, 2)
    y = np.random.randint(0, 2, 100)
    model = lgb.LGBMClassifier(n_estimators=10)
    model.fit(pd.DataFrame(X, columns=["feat1", "feat2"]), y)
    # Monkeypatch for SHAP testing
    return model

@pytest.fixture
def config():
    return {
        "model": {
            "hidden_dim": 16,
            "num_layers": 2
        },
        "training": {
            "epochs": 2
        }
    }
