<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Transaction;
use App\Http\Requests\IngestTransactionRequest;
use App\Http\Resources\TransactionResource;
use App\Services\MlScoringService;
use App\Services\RulesEngineService;
use App\Services\CaseManagerService;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;
use Illuminate\Support\Facades\DB;

class TransactionController extends Controller
{
    /**
     * Display a listing of transactions.
     */
    public function index(Request $request): AnonymousResourceCollection
    {
        $query = Transaction::with(['mlScore', 'fraudCase']);

        if ($request->has('type')) {
            $query->where('type', $request->type);
        }

        if ($request->has('channel')) {
            $query->where('channel', $request->channel);
        }

        if ($request->has('risk_level')) {
            $level = $request->risk_level;
            $query->whereHas('mlScore', function ($q) use ($level) {
                if ($level === 'high') $q->where('risk_score', '>=', 0.7);
                if ($level === 'medium') $q->whereBetween('risk_score', [0.3, 0.7]);
                if ($level === 'low') $q->where('risk_score', '<', 0.3);
            });
        }

        return TransactionResource::collection($query->orderByDesc('occurred_at')->paginate(20));
    }

    /**
     * Display the specified transaction.
     */
    public function show($id): TransactionResource
    {
        $transaction = Transaction::with(['mlScore', 'fraudCase.auditLogs', 'fraudCase.assignedAnalyst'])->findOrFail($id);
        return new TransactionResource($transaction);
    }

    /**
     * Ingest a new transaction.
     */
    public function ingest(
        IngestTransactionRequest $request,
        MlScoringService $mlService,
        RulesEngineService $rulesService,
        CaseManagerService $caseService
    ): \Illuminate\Http\JsonResponse {
        
        $transaction = DB::transaction(function () use ($request, $mlService, $rulesService, $caseService) {
            $transaction = Transaction::create($request->validated());
            
            // 1. Score the transaction
            $score = $mlService->score($transaction);
            
            // 2. Evaluate rules
            $triggeredRules = $rulesService->evaluate($transaction, $score);
            
            // 3. Create case if needed
            $caseService->createCase($transaction, $score, $triggeredRules);
            
            return $transaction;
        });

        $transaction->load(['mlScore', 'fraudCase']);

        return response()->json([
            'message' => 'Transaction ingested successfully.',
            'data' => new TransactionResource($transaction)
        ], 201);
    }

    /**
     * Return transaction's graph neighborhood data.
     */
    public function graph($id): \Illuminate\Http\JsonResponse
    {
        $transaction = Transaction::findOrFail($id);
        
        // Mock graph response
        return response()->json([
            'nodes' => [
                ['id' => 'tx_'.$transaction->id, 'label' => 'Transaction', 'type' => 'transaction'],
                ['id' => 'acc_'.$transaction->sender_account, 'label' => 'Sender', 'type' => 'account'],
                ['id' => 'acc_'.$transaction->receiver_account, 'label' => 'Receiver', 'type' => 'account'],
            ],
            'edges' => [
                ['source' => 'acc_'.$transaction->sender_account, 'target' => 'tx_'.$transaction->id, 'label' => 'sent'],
                ['source' => 'tx_'.$transaction->id, 'target' => 'acc_'.$transaction->receiver_account, 'label' => 'received'],
            ]
        ]);
    }
}
