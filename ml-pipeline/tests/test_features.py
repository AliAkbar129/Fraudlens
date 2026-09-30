import pytest
import pandas as pd
from ml_pipeline.features.tabular import TabularFeatureEngineer
from ml_pipeline.features.device import DeviceFingerprinter
from ml_pipeline.features.graph_builder import TransactionGraphBuilder
from ml_pipeline.data.augmentor import PakistanAugmentor

def test_tabular_features(sample_transaction_data):
    eng = TabularFeatureEngineer()
    df = eng.transform(sample_transaction_data)
    assert "hour_sin" in df.columns
    assert "hour_cos" in df.columns
    if "card1" in df.columns:
        assert "amt_z_score" in df.columns

def test_graph_construction(sample_transaction_data):
    builder = TransactionGraphBuilder()
    data = builder.from_dataframe(sample_transaction_data)
    assert 'transaction' in data.node_types
    assert hasattr(data['transaction'], 'x')

def test_device_fingerprinting(sample_transaction_data):
    if "DeviceInfo" not in sample_transaction_data.columns:
        sample_transaction_data["DeviceInfo"] = "Windows Mobile"
    eng = DeviceFingerprinter()
    df = eng.fit_transform(sample_transaction_data)
    assert "device_hash" in df.columns
    assert "os" in df.columns

def test_augmentor_output(sample_transaction_data):
    aug = PakistanAugmentor()
    df = aug.augment(sample_transaction_data)
    assert "wallet_transaction_type" in df.columns
    assert "pak_merchant" in df.columns

def test_feature_names_consistency():
    eng = TabularFeatureEngineer()
    df = pd.DataFrame({"TransactionDT": [1, 2], "TransactionAmt": [10, 20], "card1": [1, 1]})
    res = eng.transform(df)
    assert not res.isnull().all().all()
