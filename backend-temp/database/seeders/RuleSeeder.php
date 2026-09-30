<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Rule;
use App\Models\Analyst;

class RuleSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $admin = Analyst::where('role', 'admin')->first();

        if (!$admin) {
            return;
        }

        $rules = [
            [
                'name' => 'High Risk Auto-Flag',
                'description' => 'Automatically flag transactions with risk score > 0.7',
                'conditions' => [
                    ['field' => 'risk_score', 'operator' => '>', 'value' => 0.7],
                ],
                'action' => 'auto_flag',
                'priority' => 10,
                'created_by' => $admin->id,
                'is_active' => true,
            ],
            [
                'name' => 'Critical Amount',
                'description' => 'Escalate transactions > 100000 with moderate risk > 0.5',
                'conditions' => [
                    ['field' => 'amount', 'operator' => '>', 'value' => 100000],
                    ['field' => 'risk_score', 'operator' => '>', 'value' => 0.5],
                ],
                'action' => 'auto_escalate',
                'priority' => 20,
                'created_by' => $admin->id,
                'is_active' => true,
            ],
            [
                'name' => 'Velocity Alert',
                'description' => 'Notify if transaction velocity is high and risk is moderate',
                'conditions' => [
                    ['field' => 'risk_score', 'operator' => '>', 'value' => 0.6],
                    ['field' => 'transaction_velocity_1h', 'operator' => '>', 'value' => 5], // Mock feature
                ],
                'action' => 'notify',
                'priority' => 5,
                'created_by' => $admin->id,
                'is_active' => true,
            ],
            [
                'name' => 'Auto-Block Threshold',
                'description' => 'Block extremely high risk transactions > 0.95',
                'conditions' => [
                    ['field' => 'risk_score', 'operator' => '>', 'value' => 0.95],
                ],
                'action' => 'auto_block',
                'priority' => 100,
                'created_by' => $admin->id,
                'is_active' => true,
            ],
        ];

        foreach ($rules as $rule) {
            Rule::create($rule);
        }
    }
}
