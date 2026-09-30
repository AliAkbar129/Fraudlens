import torch
import torch.nn as nn
import torch.optim as optim
import lightgbm as lgb
import mlflow
import os
import joblib
from loguru import logger
from typing import Dict, Any

class FocalLoss(nn.Module):
    """Focal Loss for imbalanced classification."""
    def __init__(self, alpha=0.25, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        bce_loss = nn.BCEWithLogitsLoss(reduction='none')(inputs, targets)
        pt = torch.exp(-bce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * bce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss

class ModelTrainer:
    """Trains and serializes pipeline models."""
    
    def train_gnn(self, model: nn.Module, data, config: Dict[str, Any]) -> nn.Module:
        logger.info("Training GNN...")
        optimizer = optim.Adam(model.parameters(), lr=config.get('lr', 0.001))
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config.get('epochs', 100))
        criterion = FocalLoss(gamma=config.get('focal_loss_gamma', 2.0))
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        data = data.to(device)
        
        model.train()
        for epoch in range(config.get('epochs', 100)):
            optimizer.zero_grad()
            out = model(data.x_dict, data.edge_index_dict)
            
            # Assuming 'transaction' holds the labels
            targets = data['transaction'].y.float().unsqueeze(1)
            loss = criterion(out['transaction'], targets)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch} | Loss: {loss.item():.4f}")
                mlflow.log_metric("gnn_loss", loss.item(), step=epoch)
                
        return model

    def train_lgbm(self, X_train, y_train, X_val, y_val, config: Dict[str, Any]) -> lgb.LGBMClassifier:
        logger.info("Training LightGBM...")
        params = config.get('lgbm_params', {})
        params['class_weight'] = 'balanced'
        
        model = lgb.LGBMClassifier(**params, n_estimators=config.get('epochs', 100))
        
        # LightGBM v4 uses callbacks for early stopping
        callbacks = [lgb.early_stopping(stopping_rounds=config.get('early_stopping_patience', 10))]
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            callbacks=callbacks
        )
        return model

    def train_ensemble(self, ensemble, gnn_probs, lgbm_probs, y_train, y_val, val_probs):
        ensemble.stacking(gnn_probs, lgbm_probs, y_train)
        ensemble.calibrate(val_probs, y_val)
        return ensemble

    def save_models(self, gnn_model, lgbm_model, ensemble, path: str):
        logger.info(f"Saving models to {path}...")
        os.makedirs(path, exist_ok=True)
        torch.save(gnn_model.state_dict(), os.path.join(path, "gnn.pth"))
        joblib.dump(lgbm_model, os.path.join(path, "lgbm.joblib"))
        joblib.dump(ensemble, os.path.join(path, "ensemble.joblib"))

    def load_models(self, gnn_model, path: str):
        logger.info(f"Loading models from {path}...")
        gnn_model.load_state_dict(torch.load(os.path.join(path, "gnn.pth")))
        lgbm_model = joblib.load(os.path.join(path, "lgbm.joblib"))
        ensemble = joblib.load(os.path.join(path, "ensemble.joblib"))
        return gnn_model, lgbm_model, ensemble
