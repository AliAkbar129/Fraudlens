<?php

namespace App\Services;

use App\Models\Transaction;
use App\Models\MlScore;
use App\Models\Rule;
use Illuminate\Support\Collection;

class RulesEngineService
{
    /**
     * Evaluate a transaction and its score against all active rules.
     *
     * @param Transaction $transaction
     * @param MlScore $score
     * @return Collection
     */
    public function evaluate(Transaction $transaction, MlScore $score): Collection
    {
        $rules = Rule::active()->orderByDesc('priority')->get();
        $triggeredRules = collect();

        foreach ($rules as $rule) {
            $isTriggered = true;
            foreach ($rule->conditions as $condition) {
                if (!$this->evaluateCondition($condition, $transaction, $score)) {
                    $isTriggered = false;
                    break;
                }
            }

            if ($isTriggered) {
                $triggeredRules->push($rule);
                $rule->increment('hit_count');
                $rule->update(['last_triggered_at' => now()]);
            }
        }

        return $triggeredRules;
    }

    /**
     * Evaluate a single condition.
     *
     * @param array $condition
     * @param Transaction $transaction
     * @param MlScore $score
     * @return bool
     */
    protected function evaluateCondition(array $condition, Transaction $transaction, MlScore $score): bool
    {
        $field = $condition['field'];
        $operator = $condition['operator'];
        $expectedValue = $condition['value'];

        $actualValue = $this->getFieldValue($field, $transaction, $score);

        if ($actualValue === null) {
            return false;
        }

        return match ($operator) {
            '>' => $actualValue > $expectedValue,
            '<' => $actualValue < $expectedValue,
            '>=' => $actualValue >= $expectedValue,
            '<=' => $actualValue <= $expectedValue,
            '==' => $actualValue == $expectedValue,
            '!=' => $actualValue != $expectedValue,
            'in' => in_array($actualValue, (array)$expectedValue),
            'not_in' => !in_array($actualValue, (array)$expectedValue),
            'contains' => is_string($actualValue) && str_contains($actualValue, $expectedValue),
            'between' => is_array($expectedValue) && count($expectedValue) == 2 && $actualValue >= $expectedValue[0] && $actualValue <= $expectedValue[1],
            default => false,
        };
    }

    /**
     * Extract field value from transaction or score.
     */
    protected function getFieldValue(string $field, Transaction $transaction, MlScore $score): mixed
    {
        // First check ML Score fields
        $scoreAttributes = $score->getAttributes();
        if (array_key_exists($field, $scoreAttributes)) {
            return $score->$field;
        }

        // Then check Transaction fields
        $transactionAttributes = $transaction->getAttributes();
        if (array_key_exists($field, $transactionAttributes)) {
            return $transaction->$field;
        }

        // Check if it's inside raw_features
        if (is_array($transaction->raw_features) && array_key_exists($field, $transaction->raw_features)) {
            return $transaction->raw_features[$field];
        }

        return null;
    }
}
