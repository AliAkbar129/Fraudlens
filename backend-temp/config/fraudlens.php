<?php

return [
    'ml_api_url' => env('ML_API_URL', 'http://localhost:8000'),
    'ml_api_timeout' => (int) env('ML_API_TIMEOUT', 5),
    'ml_api_retries' => (int) env('ML_API_RETRIES', 2),
    
    'default_sla_hours' => [
        'critical' => 1,
        'high' => 4,
        'medium' => 24,
        'low' => 72,
    ],
    
    'auto_flag_threshold' => 0.7,
    'auto_block_threshold' => 0.95,
    
    'max_cases_per_analyst' => 20,
    
    'case_number_prefix' => 'FL',

    'api_key' => env('FRAUDLENS_API_KEY'),
];
