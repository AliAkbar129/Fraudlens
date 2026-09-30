<?php

namespace App\Services;

use App\Models\Transaction;
use App\Models\MlScore;
use App\Models\FraudCase;
use App\Models\Analyst;
use App\Models\AuditLog;
use App\Events\CaseFlagged;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

class CaseManagerService
{
    /**
     * Create a fraud case based on score and triggered rules.
     */
    public function createCase(Transaction $transaction, MlScore $score, Collection $triggeredRules): ?FraudCase
    {
        if (!$score->is_fraud_predicted && $triggeredRules->isEmpty()) {
            return null; // No case needed
        }

        $priority = $this->determinePriority($score, $triggeredRules);
        
        $case = DB::transaction(function () use ($transaction, $score, $priority, $triggeredRules) {
            $case = FraudCase::create([
                'transaction_id' => $transaction->id,
                'ml_score_id' => $score->id,
                'case_number' => $this->generateCaseNumber(),
                'status' => 'open',
                'priority' => $priority,
                'sla_deadline' => now()->addHours(config("fraudlens.default_sla_hours.{$priority}")),
            ]);

            $notes = "Case created automatically.\n";
            if ($score->is_fraud_predicted) {
                $notes .= "ML Model predicted fraud with score: {$score->risk_score}.\n";
            }
            if ($triggeredRules->isNotEmpty()) {
                $notes .= "Triggered rules: " . $triggeredRules->pluck('name')->join(', ') . ".";
            }
            
            $case->update(['analyst_notes' => $notes]);

            AuditLog::create([
                'case_id' => $case->id,
                'action' => 'created',
                'new_values' => ['priority' => $priority],
            ]);

            return $case;
        });

        // Auto-assign
        $this->autoAssign($case);

        CaseFlagged::dispatch($case);

        return $case;
    }

    /**
     * Determine priority based on risk and rules.
     */
    protected function determinePriority(MlScore $score, Collection $rules): string
    {
        $priorityValue = 0;
        
        if ($score->risk_score >= 0.9) $priorityValue = max($priorityValue, 3); // critical
        elseif ($score->risk_score >= 0.7) $priorityValue = max($priorityValue, 2); // high
        elseif ($score->risk_score >= 0.5) $priorityValue = max($priorityValue, 1); // medium

        foreach ($rules as $rule) {
            if ($rule->action === 'auto_block' || $rule->action === 'auto_escalate') {
                $priorityValue = max($priorityValue, 3);
            } elseif ($rule->action === 'auto_flag') {
                $priorityValue = max($priorityValue, 2);
            }
        }

        return match ($priorityValue) {
            3 => 'critical',
            2 => 'high',
            1 => 'medium',
            default => 'low',
        };
    }

    /**
     * Generate unique case number.
     */
    protected function generateCaseNumber(): string
    {
        $prefix = config('fraudlens.case_number_prefix', 'FL');
        $year = date('Y');
        
        $latestCase = FraudCase::where('case_number', 'like', "{$prefix}-{$year}-%")
            ->orderBy('id', 'desc')
            ->first();
            
        $sequence = 1;
        if ($latestCase) {
            $parts = explode('-', $latestCase->case_number);
            $sequence = (int) end($parts) + 1;
        }

        return sprintf("%s-%s-%06d", $prefix, $year, $sequence);
    }

    /**
     * Auto-assign case to least loaded analyst.
     */
    public function autoAssign(FraudCase $case): void
    {
        $analyst = Analyst::where('is_active', true)
            ->withCount(['assignedCases' => function ($query) {
                $query->whereIn('status', ['open', 'assigned', 'under_review']);
            }])
            ->orderBy('assigned_cases_count', 'asc')
            ->first();

        if ($analyst && $analyst->assigned_cases_count < config('fraudlens.max_cases_per_analyst', 20)) {
            $case->update([
                'assigned_analyst_id' => $analyst->id,
                'status' => 'assigned'
            ]);

            AuditLog::create([
                'case_id' => $case->id,
                'action' => 'assigned',
                'new_values' => ['assigned_analyst_id' => $analyst->id]
            ]);
        }
    }
}
