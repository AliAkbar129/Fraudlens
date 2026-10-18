import pytest
import torch
import numpy as np
from ml_pipeline.models.gnn import GraphSAGEModel, HeteroGNN
from ml_pipeline.models.baselines import BaselineModels
from ml_pipeline.models.ensemble import HybridEnsemble
from ml_pipeline.models.trainer import FocalLoss

def test_gnn_forward_shape(sample_graph_data):
    metadata = sample_graph_data.metadata()
    model = HeteroGNN(16, 1, metadata)
    out = model(sample_graph_data.x_dict, sample_graph_data.edge_index_dict)
    assert 'transaction' in out
    assert out['transaction'].shape[1] == 1

def test_lgbm_training_no_error():
    baselines = BaselineModels()
    X = np.random.rand(100, 10)
    y = np.random.randint(0, 2, 100)
    model, metrics = baselines.train_lightgbm(X, y, X, y)
    assert "roc_auc" in metrics
    assert model is not None

def test_ensemble_fusion():
    ens = HybridEnsemble()
    gnn_probs = np.array([0.1, 0.9])
    lgbm_probs = np.array([0.2, 0.8])
    fused = ens.late_fusion(gnn_probs, lgbm_probs, weight_gnn=0.5)
    assert np.allclose(fused, [0.15, 0.85])

def test_focal_loss_computation():
    criterion = FocalLoss(gamma=2.0)
    inputs = torch.tensor([[1.0], [-1.0]])
    targets = torch.tensor([[1.0], [0.0]])
    loss = criterion(inputs, targets)
    assert loss.item() > 0

def test_model_save_load(tmp_path):
    from ml_pipeline.models.trainer import ModelTrainer
    import lightgbm as lgb
    
    trainer = ModelTrainer()
    lgbm_model = lgb.LGBMClassifier(min_child_samples=1).fit([[0], [1], [2], [3]], [0, 0, 1, 1])
    ens = HybridEnsemble()
    metadata = (['transaction'], [('transaction', 'uses', 'transaction')])
    gnn_model = HeteroGNN(16, 1, metadata)
    
    gnn_model({'transaction': torch.rand(4, 2)}, {('transaction', 'uses', 'transaction'): torch.tensor([[0, 1], [1, 2]])})
    trainer.save_models(gnn_model, lgbm_model, ens, str(tmp_path))
    
    gnn2 = HeteroGNN(16, 1, metadata)
    gnn2, lgbm2, ens2 = trainer.load_models(gnn2, str(tmp_path))
    assert lgbm2 is not None
    assert ens2 is not None


def test_eval_disables_dropout(sample_graph_data):
    model = HeteroGNN(16, 1, sample_graph_data.metadata())
    model.eval()
    with torch.no_grad():
        a = model(sample_graph_data.x_dict, sample_graph_data.edge_index_dict)['transaction']
        b = model(sample_graph_data.x_dict, sample_graph_data.edge_index_dict)['transaction']
    assert torch.equal(a, b)
