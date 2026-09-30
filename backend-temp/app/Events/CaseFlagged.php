<?php

namespace App\Events;

use App\Models\FraudCase;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class CaseFlagged implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public $fraudCase;

    /**
     * Create a new event instance.
     */
    public function __construct(FraudCase $fraudCase)
    {
        $this->fraudCase = $fraudCase;
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new Channel('cases'),
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
            'case_number' => $this->fraudCase->case_number,
            'priority' => $this->fraudCase->priority,
            'status' => $this->fraudCase->status,
            'transaction_id' => $this->fraudCase->transaction_id,
            'assigned_analyst_id' => $this->fraudCase->assigned_analyst_id,
            'created_at' => $this->fraudCase->created_at->toIso8601String(),
        ];
    }
}
