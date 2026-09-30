<?php

namespace App\Events;

use App\Models\FraudCase;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class CaseResolved implements ShouldBroadcast
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
            'case_number' => $this->fraudCase->case_number,
            'status' => $this->fraudCase->status,
            'resolution' => $this->fraudCase->resolution,
            'resolved_at' => $this->fraudCase->resolved_at ? $this->fraudCase->resolved_at->toIso8601String() : null,
        ];
    }
}
