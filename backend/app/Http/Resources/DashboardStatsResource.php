<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class DashboardStatsResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'total_transactions_today' => $this->resource['total_transactions_today'] ?? 0,
            'fraud_rate' => $this->resource['fraud_rate'] ?? 0.0,
            'avg_risk_score' => $this->resource['avg_risk_score'] ?? 0.0,
            'open_cases' => $this->resource['open_cases'] ?? 0,
            'avg_latency_ms' => $this->resource['avg_latency_ms'] ?? 0,
            'model_accuracy' => $this->resource['model_accuracy'] ?? 0.0,
        ];
    }
}
