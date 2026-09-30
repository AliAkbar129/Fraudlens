<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TransactionResource extends JsonResource
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
            'transaction_ref' => $this->transaction_ref,
            'amount' => $this->amount,
            'currency' => $this->currency,
            'type' => $this->type,
            'channel' => $this->channel,
            'sender_account' => $this->sender_account,
            'receiver_account' => $this->receiver_account,
            'merchant_category' => $this->merchant_category,
            'device_info' => $this->device_info,
            'ip_address' => $this->ip_address,
            'email' => $this->email,
            'card_hash' => $this->card_hash,
            'raw_features' => $this->raw_features,
            'occurred_at' => $this->occurred_at->toIso8601String(),
            'ml_score' => new MlScoreResource($this->whenLoaded('mlScore')),
            'fraud_case' => new CaseResource($this->whenLoaded('fraudCase')),
            'created_at' => $this->created_at->toIso8601String(),
        ];
    }
}
