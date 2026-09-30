<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\FraudCase;
use App\Models\AuditLog;
use App\Http\Requests\UpdateCaseRequest;
use App\Http\Requests\ResolveCaseRequest;
use App\Http\Resources\CaseResource;
use App\Events\CaseResolved;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class CaseController extends Controller
{
    /**
     * Display a listing of cases.
     */
    public function index(Request $request): AnonymousResourceCollection
    {
        $query = FraudCase::with(['transaction', 'mlScore', 'assignedAnalyst']);

        if ($request->has('status')) {
            $query->where('status', $request->status);
        }
        
        if ($request->has('priority')) {
            $query->where('priority', $request->priority);
        }
        
        if ($request->has('analyst_id')) {
            $query->where('assigned_analyst_id', $request->analyst_id);
        }

        $sort = $request->get('sort', 'created_at');
        $dir = $request->get('dir', 'desc');
        
        $query->orderBy($sort, $dir);

        return CaseResource::collection($query->paginate(20));
    }

    /**
     * Display the specified case.
     */
    public function show($id): CaseResource
    {
        $case = FraudCase::with([
            'transaction', 
            'mlScore', 
            'assignedAnalyst',
            'auditLogs.analyst'
        ])->findOrFail($id);
        
        return new CaseResource($case);
    }

    /**
     * Update the case.
     */
    public function update(UpdateCaseRequest $request, $id): CaseResource
    {
        $case = FraudCase::findOrFail($id);
        $oldValues = $case->only($request->keys());
        
        $case->update($request->validated());

        if (!empty($oldValues)) {
            AuditLog::create([
                'case_id' => $case->id,
                'analyst_id' => request()->user()?->id,
                'action' => 'status_changed', // Simplified for demo
                'previous_values' => $oldValues,
                'new_values' => $request->validated(),
            ]);
        }

        return new CaseResource($case);
    }

    /**
     * Resolve the case.
     */
    public function resolve(ResolveCaseRequest $request, $id): \Illuminate\Http\JsonResponse
    {
        $case = FraudCase::findOrFail($id);
        
        $status = in_array($request->resolution, ['confirmed_fraud', 'legitimate', 'false_positive']) 
            ? ($request->resolution === 'confirmed_fraud' ? 'resolved_fraud' : 'resolved_legitimate') 
            : 'closed';

        $case->update([
            'status' => $status,
            'resolution' => $request->resolution,
            'resolution_reason' => $request->resolution_reason,
            'resolved_at' => now(),
        ]);

        AuditLog::create([
            'case_id' => $case->id,
            'analyst_id' => request()->user()?->id,
            'action' => 'resolved',
            'new_values' => [
                'status' => $status, 
                'resolution' => $request->resolution
            ],
        ]);

        CaseResolved::dispatch($case);

        return response()->json(['message' => 'Case resolved', 'data' => new CaseResource($case)]);
    }

    /**
     * Assign the case.
     */
    public function assign(Request $request, $id): CaseResource
    {
        $request->validate(['analyst_id' => 'required|exists:analysts,id']);
        $case = FraudCase::findOrFail($id);
        
        $case->update([
            'assigned_analyst_id' => $request->analyst_id,
            'status' => 'assigned'
        ]);

        AuditLog::create([
            'case_id' => $case->id,
            'analyst_id' => request()->user()?->id,
            'action' => 'assigned',
            'new_values' => ['assigned_analyst_id' => $request->analyst_id],
        ]);

        return new CaseResource($case);
    }

    /**
     * Escalate the case.
     */
    public function escalate($id): CaseResource
    {
        $case = FraudCase::findOrFail($id);
        
        $case->update([
            'status' => 'escalated',
            'priority' => 'critical',
        ]);

        AuditLog::create([
            'case_id' => $case->id,
            'analyst_id' => request()->user()?->id,
            'action' => 'escalated',
        ]);

        return new CaseResource($case);
    }
}
