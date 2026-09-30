<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\TransactionController;
use App\Http\Controllers\Api\CaseController;
use App\Http\Controllers\Api\AnalystController;
use App\Http\Controllers\Api\RuleController;
use App\Http\Controllers\Api\DashboardController;
use App\Http\Middleware\ApiKeyMiddleware;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
*/

Route::middleware('auth:sanctum')->group(function () {
    // Dashboard Routes
    Route::get('/dashboard/stats', [DashboardController::class, 'stats']);
    Route::get('/dashboard/graph', [DashboardController::class, 'graph']);
    Route::get('/dashboard/trends', [DashboardController::class, 'trends']);
    Route::get('/dashboard/model-performance', [DashboardController::class, 'modelPerformance']);

    // Transaction Routes
    Route::get('/transactions', [TransactionController::class, 'index']);
    Route::get('/transactions/{id}', [TransactionController::class, 'show']);
    Route::get('/transactions/{id}/graph', [TransactionController::class, 'graph']);

    // Case Routes
    Route::get('/cases', [CaseController::class, 'index']);
    Route::get('/cases/{id}', [CaseController::class, 'show']);
    Route::patch('/cases/{id}', [CaseController::class, 'update']);
    Route::post('/cases/{id}/resolve', [CaseController::class, 'resolve']);
    Route::post('/cases/{id}/assign', [CaseController::class, 'assign']);
    Route::post('/cases/{id}/escalate', [CaseController::class, 'escalate']);

    // Analyst Routes
    Route::get('/analysts', [AnalystController::class, 'index']);
    Route::get('/analysts/me', [AnalystController::class, 'profile']);
    Route::get('/analysts/{id}', [AnalystController::class, 'show']);
    Route::patch('/analysts/me', [AnalystController::class, 'updateProfile']);

    // Rule Routes
    Route::apiResource('rules', RuleController::class);
    Route::post('/rules/{id}/toggle', [RuleController::class, 'toggle']);
    Route::post('/rules/{id}/simulate', [RuleController::class, 'simulate']);
});

// Ingest Route with custom API key middleware for external service integration
Route::middleware(ApiKeyMiddleware::class)->post('/transactions/ingest', [TransactionController::class, 'ingest']);
