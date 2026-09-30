import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score
import xgboost as xgb
import lightgbm as lgb
import mlflow
from loguru import logger

class BaselineModels:
    """Baseline classification models."""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}

    def _evaluate(self, model, X_test, y_test) -> dict:
        probs = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
        pr = average_precision_score(y_test, probs)
        return {"roc_auc": auc, "pr_auc": pr}

    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        logger.info("Training Logistic Regression...")
        model = LogisticRegression(class_weight="balanced", random_state=self.random_state, max_iter=1000)
        model.fit(X_train, y_train)
        metrics = self._evaluate(model, X_test, y_test)
        self.models['lr'] = model
        return model, metrics

    def train_random_forest(self, X_train, y_train, X_test, y_test):
        logger.info("Training Random Forest...")
        model = RandomForestClassifier(class_weight="balanced", n_estimators=100, random_state=self.random_state, n_jobs=-1)
        model.fit(X_train, y_train)
        metrics = self._evaluate(model, X_test, y_test)
        self.models['rf'] = model
        return model, metrics

    def train_xgboost(self, X_train, y_train, X_test, y_test):
        logger.info("Training XGBoost...")
        scale_pos_weight = (len(y_train) - y_train.sum()) / max(y_train.sum(), 1)
        model = xgb.XGBClassifier(scale_pos_weight=scale_pos_weight, random_state=self.random_state, n_estimators=100)
        model.fit(X_train, y_train)
        metrics = self._evaluate(model, X_test, y_test)
        self.models['xgb'] = model
        return model, metrics

    def train_lightgbm(self, X_train, y_train, X_test, y_test):
        logger.info("Training LightGBM...")
        scale_pos_weight = (len(y_train) - y_train.sum()) / max(y_train.sum(), 1)
        model = lgb.LGBMClassifier(scale_pos_weight=scale_pos_weight, random_state=self.random_state, n_estimators=100)
        model.fit(X_train, y_train)
        metrics = self._evaluate(model, X_test, y_test)
        self.models['lgbm'] = model
        return model, metrics

    def train_all(self, X_train, y_train, X_test, y_test) -> pd.DataFrame:
        """Trains all baselines and returns comparison."""
        results = []
        for name, train_func in [
            ("Logistic Regression", self.train_logistic_regression),
            ("Random Forest", self.train_random_forest),
            ("XGBoost", self.train_xgboost),
            ("LightGBM", self.train_lightgbm)
        ]:
            _, metrics = train_func(X_train, y_train, X_test, y_test)
            metrics["Model"] = name
            results.append(metrics)
            
        return pd.DataFrame(results).set_index("Model")
