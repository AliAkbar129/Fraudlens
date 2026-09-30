import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from loguru import logger
import torch
import lightgbm as lgb
from typing import Union

class HybridEnsemble:
    """Combines GNN and LightGBM models."""
    
    def __init__(self):
        self.meta_learner = LogisticRegression(class_weight="balanced")
        self.calibrator = None
        self.is_fitted = False

    def late_fusion(self, gnn_probs: np.ndarray, lgbm_probs: np.ndarray, weight_gnn: float = 0.4) -> np.ndarray:
        """Simple weighted average."""
        return weight_gnn * gnn_probs + (1 - weight_gnn) * lgbm_probs

    def stacking(self, gnn_probs: np.ndarray, lgbm_probs: np.ndarray, y_train: np.ndarray):
        """Trains meta-learner on out-of-fold predictions."""
        logger.info("Training stacking meta-learner...")
        X_meta = np.column_stack((gnn_probs, lgbm_probs))
        self.meta_learner.fit(X_meta, y_train)
        self.is_fitted = True

    def calibrate(self, probs: np.ndarray, y_true: np.ndarray):
        """Platt scaling for calibration."""
        logger.info("Calibrating ensemble probabilities...")
        # CalibratedClassifierCV requires an estimator. 
        # For precomputed probs, we can use a dummy logistic regression.
        dummy_lr = LogisticRegression()
        self.calibrator = CalibratedClassifierCV(dummy_lr, method="sigmoid", cv="prefit")
        self.calibrator.fit(probs.reshape(-1, 1), y_true)

    def predict(self, transaction_features: pd.DataFrame, graph_data, gnn_model: torch.nn.Module, lgbm_model: lgb.LGBMClassifier, method="stacking", weight_gnn=0.4) -> np.ndarray:
        """Full pipeline prediction."""
        # 1. GNN Prediction
        gnn_model.eval()
        with torch.no_grad():
            gnn_out = gnn_model(graph_data.x_dict, graph_data.edge_index_dict)
            gnn_logits = gnn_out['transaction']
            gnn_probs = torch.sigmoid(gnn_logits).cpu().numpy().flatten()
            
        # 2. LGBM Prediction
        lgbm_probs = lgbm_model.predict_proba(transaction_features)[:, 1]
        
        # 3. Fuse
        if method == "stacking" and self.is_fitted:
            X_meta = np.column_stack((gnn_probs, lgbm_probs))
            fused_probs = self.meta_learner.predict_proba(X_meta)[:, 1]
        else:
            fused_probs = self.late_fusion(gnn_probs, lgbm_probs, weight_gnn)
            
        # 4. Calibrate
        if self.calibrator is not None:
            final_probs = self.calibrator.predict_proba(fused_probs.reshape(-1, 1))[:, 1]
        else:
            final_probs = fused_probs
            
        return final_probs
