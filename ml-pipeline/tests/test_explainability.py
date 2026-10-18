import pytest
import json
import pandas as pd
from ml_pipeline.explainability.shap_explainer import SHAPExplainer
from ml_pipeline.explainability.gnn_explainer import GNNExplainerWrapper
from ml_pipeline.explainability.unified import UnifiedExplainer

def test_shap_output_serializable(trained_lgbm_model):
    explainer = SHAPExplainer(trained_lgbm_model)
    features = {"feat1": 1.0, "feat2": 2.0}
    explanation = explainer.explain_single(features)
    assert "top_features" in explanation
    # Test JSON serialization
    json_str = json.dumps(explanation)
    assert isinstance(json_str, str)

def test_gnn_explanation_subgraph(sample_graph_data):
    from ml_pipeline.models.gnn import HeteroGNN
    metadata = sample_graph_data.metadata()
    model = HeteroGNN(16, 1, metadata)
    wrapper = GNNExplainerWrapper(model, epochs=1)
    
    explanation = wrapper.explain_node(sample_graph_data, 0)
    subgraph = wrapper.extract_fraud_subgraph(explanation, threshold=0.0)
    assert isinstance(subgraph, list)
    assert explanation["edge_mask"]
    for edge_type, mask in explanation["edge_mask"].items():
        assert mask.shape[0] == sample_graph_data[edge_type].edge_index.shape[1]
        assert mask.isfinite().all()

def test_unified_explanation_has_required_fields(trained_lgbm_model, sample_graph_data):
    from ml_pipeline.models.gnn import HeteroGNN
    metadata = sample_graph_data.metadata()
    model = HeteroGNN(16, 1, metadata)
    
    shap_exp = SHAPExplainer(trained_lgbm_model)
    gnn_exp = GNNExplainerWrapper(model, epochs=1)
    unified = UnifiedExplainer(shap_exp, gnn_exp)
    
    result = unified.explain_transaction("tx123", {"feat1": 1.0, "feat2": 2.0}, sample_graph_data, 0, 0.95)
    
    assert "transaction_id" in result
    assert "risk_score" in result
    assert "tabular_explanation" in result
    assert "graph_explanation" in result
    assert "summary" in result

def test_explanation_summary_human_readable(trained_lgbm_model, sample_graph_data):
    from ml_pipeline.models.gnn import HeteroGNN
    metadata = sample_graph_data.metadata()
    model = HeteroGNN(16, 1, metadata)
    
    shap_exp = SHAPExplainer(trained_lgbm_model)
    gnn_exp = GNNExplainerWrapper(model, epochs=1)
    unified = UnifiedExplainer(shap_exp, gnn_exp)
    
    result = unified.explain_transaction("tx123", {"feat1": 1.0, "feat2": 2.0}, sample_graph_data, 0, 0.95)
    assert isinstance(result["summary"], str)
    assert "risk score" in result["summary"]


def test_shap_rejects_wrong_feature_schema(trained_lgbm_model):
    with pytest.raises(ValueError, match='schema'):
        SHAPExplainer(trained_lgbm_model).explain_single({'wrong': 1})
