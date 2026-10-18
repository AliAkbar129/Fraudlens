<?php
namespace Tests\Feature;
use Tests\TestCase;
use Illuminate\Support\Facades\Http;
use App\Services\MlScoringService;
use App\Models\Transaction;

class ApiSafetyTest extends TestCase
{
    public function test_api_routes_are_registered_and_guarded(): void
    {
        $this->getJson('/api/transactions')->assertUnauthorized();
        $this->postJson('/api/transactions/ingest', [])->assertUnauthorized();
    }
    public function test_unavailable_model_does_not_become_zero_risk(): void
    {
        config(['fraudlens.ml_api_retries' => 1]);
        Http::fake(['*' => Http::response(['detail' => 'not trained'], 503)]);
        $transaction = new Transaction(['transaction_ref' => 'test', 'amount' => 12, 'occurred_at' => now()]);
        $this->expectException(\RuntimeException::class);
        app(MlScoringService::class)->score($transaction);
    }
}
