<?php

namespace App\Events;

use App\Models\MlScore;
use App\Models\Transaction;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class TransactionScored implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $transaction;
    public $mlScore;

    /**
     * Create a new event instance.
     */
    public function __construct(Transaction $transaction, MlScore $mlScore)
    {
        $this->transaction = $transaction;
        $this->mlScore = $mlScore;
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new Channel('dashboard'),
        ];
    }

    /**
     * Get the data to broadcast.
     *
     * @return array<string, mixed>
     */
    public function broadcastWith(): array
    {
        return [
            'transaction_ref' => $this->transaction->transaction_ref,
            'risk_score' => $this->mlScore->risk_score,
            'is_fraud_predicted' => $this->mlScore->is_fraud_predicted,
            'amount' => $this->transaction->amount,
            'occurred_at' => $this->transaction->occurred_at->toIso8601String(),
        ];
    }
}
