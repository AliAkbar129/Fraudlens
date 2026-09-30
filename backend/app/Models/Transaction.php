<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Database\Eloquent\Builder;

class Transaction extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'transaction_ref',
        'amount',
        'currency',
        'type',
        'channel',
        'sender_account',
        'receiver_account',
        'merchant_category',
        'device_info',
        'ip_address',
        'email',
        'card_hash',
        'raw_features',
        'occurred_at',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'amount' => 'decimal:2',
        'raw_features' => 'array',
        'occurred_at' => 'datetime',
    ];

    /**
     * Get the ML score associated with the transaction.
     *
     * @return HasOne
     */
    public function mlScore(): HasOne
    {
        return $this->hasOne(MlScore::class);
    }

    /**
     * Get the fraud case associated with the transaction.
     *
     * @return HasOne
     */
    public function fraudCase(): HasOne
    {
        return $this->hasOne(FraudCase::class);
    }

    /**
     * Scope a query to only include fraudulent transactions.
     *
     * @param Builder $query
     * @return Builder
     */
    public function scopeFraudulent(Builder $query): Builder
    {
        return $query->whereHas('fraudCase', function ($q) {
            $q->where('resolution', 'confirmed_fraud');
        });
    }
}
