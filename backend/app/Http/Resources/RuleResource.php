<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class RuleResource extends JsonResource
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
            'name' => $this->name,
            'description' => $this->description,
            'conditions' => $this->conditions,
            'action' => $this->action,
            'priority' => $this->priority,
            'is_active' => $this->is_active,
            'hit_count' => $this->hit_count,
            'last_triggered_at' => $this->last_triggered_at ? $this->last_triggered_at->toIso8601String() : null,
            'created_by' => new AnalystResource($this->whenLoaded('creator')),
            'created_at' => $this->created_at->toIso8601String(),
            'updated_at' => $this->updated_at->toIso8601String(),
        ];
    }
}
