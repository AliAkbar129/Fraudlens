from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TransactionInput(BaseModel):
    transaction_id: str
    amount: float = Field(..., gt=0)
    card_id: str
    device_info: Optional[str] = None
    email_domain: Optional[str] = None
    time_step: float

class PredictionResponse(BaseModel):
    transaction_id: str
    risk_score: float = Field(..., ge=0, le=1)
    gnn_score: float
    lgbm_score: float
    is_fraud: bool
    confidence: float
    explanation: Optional[Dict[str, Any]] = None

class BatchPredictionRequest(BaseModel):
    transactions: List[TransactionInput]

class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]

class HealthResponse(BaseModel):
    status: str
    model_version: str
    uptime: float
    gpu_available: bool

class ModelInfoResponse(BaseModel):
    model_type: str
    version: str
    metrics: Dict[str, float]
    last_trained: str

class ExplanationResponse(BaseModel):
    transaction_id: str
    risk_score: float
    tabular_explanation: Dict[str, Any]
    graph_explanation: Dict[str, Any]
    summary: str
