import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import time
import base64
import io
import matplotlib.pyplot as plt
from loguru import logger

class ModelEvaluator:
    """Evaluates fraud detection models."""
    
    def compute_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
        """Computes core classification metrics."""
        return {
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "auc_roc": roc_auc_score(y_true, y_proba),
            "auc_pr": average_precision_score(y_true, y_proba),
            "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
            "classification_report": classification_report(y_true, y_pred, output_dict=True)
        }

    def evaluate_at_thresholds(self, y_true: np.ndarray, y_proba: np.ndarray, thresholds: list) -> pd.DataFrame:
        """Evaluates metrics at multiple decision thresholds."""
        results = []
        for t in thresholds:
            preds = (y_proba >= t).astype(int)
            res = self.compute_metrics(y_true, preds, y_proba)
            res["threshold"] = t
            results.append(res)
        return pd.DataFrame(results)

    def plot_curves(self, y_true: np.ndarray, y_proba: np.ndarray) -> dict:
        """Generates ROC and PR curves as base64 images."""
        plt.style.use('ggplot')
        plots = {}
        
        # ROC
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        plt.figure(figsize=(6, 4))
        plt.plot(fpr, tpr, label=f"AUC = {roc_auc_score(y_true, y_proba):.3f}")
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        plots['roc'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # PR
        p, r, _ = precision_recall_curve(y_true, y_proba)
        plt.figure(figsize=(6, 4))
        plt.plot(r, p, label=f"AP = {average_precision_score(y_true, y_proba):.3f}")
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        plots['pr'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return plots

    def compare_models(self, results_dict: dict) -> pd.DataFrame:
        """Compares metrics across multiple models."""
        return pd.DataFrame(results_dict).T

    def benchmark_latency(self, model_func, sample_data, n_runs=100) -> dict:
        """Benchmarks inference latency."""
        latencies = []
        # Warmup
        for _ in range(10):
            _ = model_func(sample_data)
            
        for _ in range(n_runs):
            start = time.perf_counter()
            _ = model_func(sample_data)
            latencies.append((time.perf_counter() - start) * 1000) # ms
            
        return {
            "p50": np.percentile(latencies, 50),
            "p95": np.percentile(latencies, 95),
            "p99": np.percentile(latencies, 99),
            "mean": np.mean(latencies)
        }

    def generate_report(self, all_results: dict) -> dict:
        """Compiles full evaluation report."""
        logger.info("Generating evaluation report...")
        return {
            "timestamp": time.time(),
            "metrics": all_results.get("metrics", {}),
            "latency": all_results.get("latency", {})
        }
