<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Builder;

class FraudCase extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'transaction_id',
        'ml_score_id',
        'case_number',
        'status',
        'priority',
        'assigned_analyst_id',
        'analyst_notes',
        'resolution',
        'resolution_reason',
        'sla_deadline',
        'resolved_at',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'sla_deadline' => 'datetime',
        'resolved_at' => 'datetime',
    ];

    /**
     * Get the transaction associated with the case.
     *
     * @return BelongsTo
     */
    public function transaction(): BelongsTo
    {
        return $this->belongsTo(Transaction::class);
    }

    /**
     * Get the ML score associated with the case.
     *
     * @return BelongsTo
     */
    public function mlScore(): BelongsTo
    {
        return $this->belongsTo(MlScore::class);
    }

    /**
     * Get the assigned analyst.
     *
     * @return BelongsTo
     */
    public function assignedAnalyst(): BelongsTo
    {
        return $this->belongsTo(Analyst::class, 'assigned_analyst_id');
    }

    /**
     * Get the audit logs for the case.
     *
     * @return HasMany
     */
    public function auditLogs(): HasMany
    {
        return $this->hasMany(AuditLog::class, 'case_id');
    }

    /**
     * Scope a query to only include open cases.
     *
     * @param Builder $query
     * @return Builder
     */
    public function scopeOpen(Builder $query): Builder
    {
        return $query->whereIn('status', ['open', 'assigned', 'under_review', 'escalated']);
    }

    /**
     * Scope a query to only include high priority cases.
     *
     * @param Builder $query
     * @return Builder
     */
    public function scopeHighPriority(Builder $query): Builder
    {
        return $query->whereIn('priority', ['critical', 'high']);
    }

    /**
     * Scope a query to include only unresolved cases that breached SLA.
     *
     * @param Builder $query
     * @return Builder
     */
    public function scopeSlaBreached(Builder $query): Builder
    {
        return $query->whereNull('resolved_at')
                     ->where('sla_deadline', '<', now());
    }
}
