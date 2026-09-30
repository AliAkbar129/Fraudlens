<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasOne;

class MlScore extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'transaction_id',
        'risk_score',
        'gnn_score',
        'lgbm_score',
        'ensemble_method',
        'model_version',
        'shap_explanation',
        'gnn_explanation',
        'unified_explanation',
        'latency_ms',
        'is_fraud_predicted',
        'confidence',
        'scored_at',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'risk_score' => 'float',
        'gnn_score' => 'float',
        'lgbm_score' => 'float',
        'shap_explanation' => 'array',
        'gnn_explanation' => 'array',
        'unified_explanation' => 'array',
        'latency_ms' => 'integer',
        'is_fraud_predicted' => 'boolean',
        'confidence' => 'float',
        'scored_at' => 'datetime',
    ];

    /**
     * Get the transaction that owns the score.
     *
     * @return BelongsTo
     */
    public function transaction(): BelongsTo
    {
        return $this->belongsTo(Transaction::class);
    }

    /**
     * Get the fraud case associated with the score.
     *
     * @return HasOne
     */
    public function fraudCase(): HasOne
    {
        return $this->hasOne(FraudCase::class);
    }
}
