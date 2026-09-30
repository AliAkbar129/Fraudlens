<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Transaction;
use App\Models\FraudCase;
use App\Models\MlScore;
use App\Http\Resources\DashboardStatsResource;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    /**
     * Get dashboard stats.
     */
    public function stats(): DashboardStatsResource
    {
        $today = today();
        
        $totalTxs = Transaction::whereDate('occurred_at', $today)->count();
        $fraudCases = FraudCase::whereDate('created_at', $today)->count();
        
        $stats = [
            'total_transactions_today' => $totalTxs,
            'fraud_rate' => $totalTxs > 0 ? round(($fraudCases / $totalTxs) * 100, 2) : 0,
            'avg_risk_score' => MlScore::whereDate('scored_at', $today)->avg('risk_score') ?? 0,
            'open_cases' => FraudCase::open()->count(),
            'avg_latency_ms' => MlScore::whereDate('scored_at', $today)->avg('latency_ms') ?? 0,
            'model_accuracy' => 94.5, // Mocked
        ];

        return new DashboardStatsResource($stats);
    }

    /**
     * Get graph data.
     */
    public function graph(): \Illuminate\Http\JsonResponse
    {
        return response()->json([
            'nodes' => [
                ['id' => '1', 'label' => 'Acc A', 'type' => 'account', 'risk' => 0.1],
                ['id' => '2', 'label' => 'Acc B', 'type' => 'account', 'risk' => 0.8],
                ['id' => '3', 'label' => 'Tx 101', 'type' => 'transaction', 'risk' => 0.9],
            ],
            'edges' => [
                ['source' => '1', 'target' => '3'],
                ['source' => '3', 'target' => '2'],
            ]
        ]);
    }

    /**
     * Get trends data.
     */
    public function trends(): \Illuminate\Http\JsonResponse
    {
        return response()->json([
            'labels' => ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'datasets' => [
                [
                    'label' => 'Fraud Cases',
                    'data' => [12, 19, 15, 22, 30, 25, 18]
                ]
            ]
        ]);
    }

    /**
     * Get model performance data.
     */
    public function modelPerformance(): \Illuminate\Http\JsonResponse
    {
        return response()->json([
            'precision' => [0.85, 0.86, 0.88, 0.87],
            'recall' => [0.90, 0.91, 0.89, 0.92],
            'f1_score' => [0.87, 0.88, 0.88, 0.89],
            'auc' => [0.95, 0.96, 0.95, 0.97],
            'dates' => ['2024-01', '2024-02', '2024-03', '2024-04']
        ]);
    }
}
