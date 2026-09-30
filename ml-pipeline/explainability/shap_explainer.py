import shap
import pandas as pd
import numpy as np
import lightgbm as lgb
from loguru import logger
import json

class SHAPExplainer:
    """SHAP explainer for tabular Tree models."""
    
    def __init__(self, model: lgb.LGBMClassifier):
        self.model = model
        self.explainer = shap.TreeExplainer(model)

    def explain_single(self, features_dict: dict, top_k: int = 5) -> dict:
        """Explains a single transaction."""
        df = pd.DataFrame([features_dict])
        shap_values = self.explainer.shap_values(df)
        
        # Handle SHAP output structures for different TreeExplainers
        if isinstance(shap_values, list):
            sv = shap_values[1][0]
        else:
            sv = shap_values[0]
            
        base_value = self.explainer.expected_value
        if isinstance(base_value, list) or isinstance(base_value, np.ndarray):
            base_value = base_value[1] if len(base_value) > 1 else base_value[0]
            
        feature_names = df.columns
        importances = []
        for i, val in enumerate(sv):
            importances.append({
                "name": feature_names[i],
                "value": float(df.iloc[0, i]),
                "shap_value": float(val),
                "direction": "increases_risk" if val > 0 else "decreases_risk",
                "description": f"Feature {feature_names[i]} value {df.iloc[0, i]}"
            })
            
        importances = sorted(importances, key=lambda x: abs(x["shap_value"]), reverse=True)[:top_k]
        
        return {
            "base_value": float(base_value),
            "top_features": importances
        }

    def explain_batch(self, features_df: pd.DataFrame) -> list:
        """Explains a batch of transactions."""
        results = []
        for i in range(len(features_df)):
            results.append(self.explain_single(features_df.iloc[i].to_dict()))
        return results

    def get_feature_importance(self) -> dict:
        """Global feature importance."""
        if hasattr(self.model, "feature_importances_"):
            imp = self.model.feature_importances_
            names = self.model.feature_name_
            return {names[i]: float(imp[i]) for i in range(len(names))}
        return {}

    def to_json(self, explanation: dict) -> str:
        """Serializes explanation to JSON."""
        return json.dumps(explanation)
