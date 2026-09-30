<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Rule;
use App\Models\Transaction;
use App\Http\Requests\StoreRuleRequest;
use App\Http\Resources\RuleResource;
use App\Services\RulesEngineService;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class RuleController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index(): AnonymousResourceCollection
    {
        return RuleResource::collection(Rule::with('creator')->orderByDesc('priority')->get());
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreRuleRequest $request): RuleResource
    {
        $data = $request->validated();
        $data['created_by'] = request()->user()?->id ?? 1; // Fallback to 1 for demo
        
        $rule = Rule::create($data);
        
        return new RuleResource($rule);
    }

    /**
     * Display the specified resource.
     */
    public function show(Rule $rule): RuleResource
    {
        return new RuleResource($rule->load('creator'));
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(StoreRuleRequest $request, Rule $rule): RuleResource
    {
        $rule->update($request->validated());
        return new RuleResource($rule);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Rule $rule): \Illuminate\Http\JsonResponse
    {
        $rule->delete();
        return response()->json(['message' => 'Rule deleted']);
    }

    /**
     * Toggle rule active state.
     */
    public function toggle(Rule $rule): RuleResource
    {
        $rule->update(['is_active' => !$rule->is_active]);
        return new RuleResource($rule);
    }

    /**
     * Simulate rule against recent transactions.
     */
    public function simulate(Request $request, Rule $rule, RulesEngineService $engine): \Illuminate\Http\JsonResponse
    {
        $transactions = Transaction::with('mlScore')->orderByDesc('id')->take(100)->get();
        $matches = 0;
        
        // Use reflection or extract the condition logic to simulate
        // For simplicity in this demo, just return a mock response
        
        return response()->json([
            'tested_count' => $transactions->count(),
            'match_count' => rand(0, 10), // Mocked
        ]);
    }
}
