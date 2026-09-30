<?php

namespace App\Services;

use App\Models\Transaction;
use App\Models\MlScore;
use App\Events\TransactionScored;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Exception;

class MlScoringService
{
    protected string $apiUrl;
    protected int $timeout;
    protected int $retries;

    public function __construct()
    {
        $this->apiUrl = config('fraudlens.ml_api_url') . '/predict';
        $this->timeout = config('fraudlens.ml_api_timeout');
        $this->retries = config('fraudlens.ml_api_retries');
    }

    /**
     * Score a transaction synchronously.
     *
     * @param Transaction $transaction
     * @return MlScore
     */
    public function score(Transaction $transaction): MlScore
    {
        $payload = $this->buildPayload($transaction);
        $start = microtime(true);
        $latencyMs = 0;

        try {
            $response = Http::timeout($this->timeout)
                ->retry($this->retries, 100)
                ->post($this->apiUrl, $payload);
            
            $latencyMs = (int) ((microtime(true) - $start) * 1000);

            if ($response->successful()) {
                $data = $response->json();
                return $this->storeScore($transaction, $data, $latencyMs);
            }
            
            Log::error('ML API Error', ['status' => $response->status(), 'body' => $response->body()]);
        } catch (Exception $e) {
            Log::error('ML API Exception: ' . $e->getMessage());
            $latencyMs = (int) ((microtime(true) - $start) * 1000);
        }

        // Fallback scoring if ML API fails
        return $this->fallbackScoring($transaction, $latencyMs);
    }

    /**
     * Store the ML score.
     */
    protected function storeScore(Transaction $transaction, array $data, int $latencyMs): MlScore
    {
        $score = MlScore::create([
            'transaction_id' => $transaction->id,
            'risk_score' => $data['risk_score'] ?? 0.5,
            'gnn_score' => $data['gnn_score'] ?? null,
            'lgbm_score' => $data['lgbm_score'] ?? null,
            'ensemble_method' => $data['ensemble_method'] ?? 'default',
            'model_version' => $data['model_version'] ?? '1.0',
            'shap_explanation' => $data['shap_explanation'] ?? null,
            'gnn_explanation' => $data['gnn_explanation'] ?? null,
            'unified_explanation' => $data['unified_explanation'] ?? null,
            'latency_ms' => $latencyMs,
            'is_fraud_predicted' => ($data['risk_score'] ?? 0.5) > config('fraudlens.auto_flag_threshold', 0.7),
            'confidence' => $data['confidence'] ?? 0.8,
            'scored_at' => now(),
        ]);

        TransactionScored::dispatch($transaction, $score);

        return $score;
    }

    /**
     * Fallback scoring when API is unavailable.
     */
    protected function fallbackScoring(Transaction $transaction, int $latencyMs): MlScore
    {
        $score = MlScore::create([
            'transaction_id' => $transaction->id,
            'risk_score' => 0.0, // Default to lowest risk on failure, or could be static logic
            'model_version' => 'fallback',
            'latency_ms' => $latencyMs,
            'is_fraud_predicted' => false,
            'scored_at' => now(),
        ]);

        TransactionScored::dispatch($transaction, $score);

        return $score;
    }

    /**
     * Build the payload for the ML API.
     */
    protected function buildPayload(Transaction $transaction): array
    {
        return [
            'transaction_id' => $transaction->transaction_ref,
            'amount' => (float) $transaction->amount,
            'currency' => $transaction->currency,
            'type' => $transaction->type,
            'channel' => $transaction->channel,
            'sender_account' => $transaction->sender_account,
            'receiver_account' => $transaction->receiver_account,
            'merchant_category' => $transaction->merchant_category,
            'ip_address' => $transaction->ip_address,
            'card_hash' => $transaction->card_hash,
            'raw_features' => $transaction->raw_features,
            'occurred_at' => $transaction->occurred_at->toIso8601String(),
        ];
    }
}
