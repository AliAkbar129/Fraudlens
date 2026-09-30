<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class CaseResource extends JsonResource
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
            'case_number' => $this->case_number,
            'status' => $this->status,
            'priority' => $this->priority,
            'assigned_analyst' => new AnalystResource($this->whenLoaded('assignedAnalyst')),
            'analyst_notes' => $this->analyst_notes,
            'resolution' => $this->resolution,
            'resolution_reason' => $this->resolution_reason,
            'sla_deadline' => $this->sla_deadline ? $this->sla_deadline->toIso8601String() : null,
            'resolved_at' => $this->resolved_at ? $this->resolved_at->toIso8601String() : null,
            'transaction' => new TransactionResource($this->whenLoaded('transaction')),
            'ml_score' => new MlScoreResource($this->whenLoaded('mlScore')),
            'audit_logs' => $this->whenLoaded('auditLogs'),
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
        ];
    }
}
