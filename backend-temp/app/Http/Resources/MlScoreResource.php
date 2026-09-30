<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class MlScoreResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'transaction_id' => $this->transaction_id,
            'risk_score' => $this->risk_score,
            'gnn_score' => $this->gnn_score,
            'lgbm_score' => $this->lgbm_score,
            'ensemble_method' => $this->ensemble_method,
            'model_version' => $this->model_version,
            'shap_explanation' => $this->shap_explanation,
            'gnn_explanation' => $this->gnn_explanation,
            'unified_explanation' => $this->unified_explanation,
            'latency_ms' => $this->latency_ms,
            'is_fraud_predicted' => $this->is_fraud_predicted,
            'confidence' => $this->confidence,
            'scored_at' => $this->scored_at->toIso8601String(),
        ];
    }
}
