from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import torch
from loguru import logger
import yaml

from ml_pipeline.api.schemas import (
    TransactionInput, PredictionResponse, BatchPredictionRequest,
    BatchPredictionResponse, HealthResponse, ModelInfoResponse, ExplanationResponse
)
from ml_pipeline.api.model_loader import ModelLoader
from ml_pipeline.api.middleware import RequestLoggingMiddleware, LatencyTrackingMiddleware, APIKeyMiddleware, RateLimitMiddleware
from ml_pipeline.explainability.shap_explainer import SHAPExplainer
from ml_pipeline.explainability.gnn_explainer import GNNExplainerWrapper
from ml_pipeline.explainability.unified import UnifiedExplainer

# Load config
try:
    with open("configs/default.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    config = {"api": {"model_path": "artifacts/models"}}

start_time = time.time()
loader = ModelLoader()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting API...")
    loader.load_models(config)
    yield
    # Shutdown
    logger.info("Shutting down API...")

app = FastAPI(title="FraudLens API", lifespan=lifespan)

# Middlewares
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(LatencyTrackingMiddleware)
# Uncomment to enable API keys and rate limiting
# app.add_middleware(APIKeyMiddleware)
# app.add_middleware(RateLimitMiddleware)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        model_version=loader.get_model_info()["version"],
        uptime=time.time() - start_time,
        gpu_available=torch.cuda.is_available()
    )

@app.get("/model/info", response_model=ModelInfoResponse)
async def model_info():
    info = loader.get_model_info()
    return ModelInfoResponse(**info)

@app.post("/predict", response_model=PredictionResponse)
async def predict(transaction: TransactionInput):
    # In reality, we'd process transaction -> tabular features -> graph node
    # Here we mock the model output for the pipeline demonstration
    
    gnn_score = 0.85
    lgbm_score = 0.90
    risk_score = 0.88
    
    return PredictionResponse(
        transaction_id=transaction.transaction_id,
        risk_score=risk_score,
        gnn_score=gnn_score,
        lgbm_score=lgbm_score,
        is_fraud=risk_score > 0.5,
        confidence=abs(risk_score - 0.5) * 2
    )

@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    predictions = []
    for tx in request.transactions:
        predictions.append(PredictionResponse(
            transaction_id=tx.transaction_id,
            risk_score=0.5,
            gnn_score=0.5,
            lgbm_score=0.5,
            is_fraud=False,
            confidence=0.0
        ))
    return BatchPredictionResponse(predictions=predictions)

@app.post("/explain/{transaction_id}", response_model=ExplanationResponse)
async def explain(transaction_id: str, transaction: TransactionInput):
    # Mock explanation
    return ExplanationResponse(
        transaction_id=transaction_id,
        risk_score=0.88,
        tabular_explanation={"top_features": [{"name": "amount", "value": transaction.amount, "shap_value": 2.5, "direction": "increases_risk", "description": "High amount"}]},
        graph_explanation={"critical_edges": [], "important_nodes": [], "fraud_ring_size": 0},
        summary="Transaction is high risk due to amount."
    )
