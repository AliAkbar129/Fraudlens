<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\Analyst;
use Illuminate\Support\Str;

class AnalystSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $analysts = [
            [
                'name' => 'Admin User',
                'email' => 'admin@fraudlens.com',
                'password' => Hash::make('password'),
                'role' => 'admin',
                'api_key' => Str::random(64),
                'permissions' => json_encode(['all']),
            ],
            [
                'name' => 'Senior Analyst 1',
                'email' => 'senior1@fraudlens.com',
                'password' => Hash::make('password'),
                'role' => 'senior_analyst',
                'api_key' => Str::random(64),
                'permissions' => json_encode(['manage_cases', 'manage_rules']),
            ],
            [
                'name' => 'Senior Analyst 2',
                'email' => 'senior2@fraudlens.com',
                'password' => Hash::make('password'),
                'role' => 'senior_analyst',
                'api_key' => Str::random(64),
                'permissions' => json_encode(['manage_cases', 'manage_rules']),
            ],
            [
                'name' => 'Analyst 1',
                'email' => 'analyst1@fraudlens.com',
                'password' => Hash::make('password'),
                'role' => 'analyst',
                'api_key' => Str::random(64),
                'permissions' => json_encode(['manage_cases']),
            ],
            [
                'name' => 'Analyst 2',
                'email' => 'analyst2@fraudlens.com',
                'password' => Hash::make('password'),
                'role' => 'analyst',
                'api_key' => Str::random(64),
                'permissions' => json_encode(['manage_cases']),
            ],
        ];

        foreach ($analysts as $analyst) {
            Analyst::create($analyst);
        }
    }
}
