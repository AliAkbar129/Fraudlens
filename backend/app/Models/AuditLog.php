<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class AuditLog extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'case_id',
        'analyst_id',
        'action',
        'previous_values',
        'new_values',
        'ip_address',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'previous_values' => 'array',
        'new_values' => 'array',
    ];

    /**
     * Get the case associated with the log.
     *
     * @return BelongsTo
     */
    public function fraudCase(): BelongsTo
    {
        return $this->belongsTo(FraudCase::class, 'case_id');
    }

    /**
     * Get the analyst who performed the action.
     *
     * @return BelongsTo
     */
    public function analyst(): BelongsTo
    {
        return $this->belongsTo(Analyst::class, 'analyst_id');
    }
}
