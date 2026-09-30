<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class AnalystResource extends JsonResource
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
            'email' => $this->email,
            'role' => $this->role,
            'permissions' => $this->permissions,
            'is_active' => $this->is_active,
            'last_login_at' => $this->last_login_at ? $this->last_login_at->toIso8601String() : null,
            'stats' => $this->when(isset($this->stats), $this->stats),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}
