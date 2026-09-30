<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('ml_scores', function (Blueprint $table) {
            $table->id();
            $table->foreignId('transaction_id')->constrained()->onDelete('cascade');
            $table->float('risk_score', 8, 4); // 0-1
            $table->float('gnn_score', 8, 4)->nullable();
            $table->float('lgbm_score', 8, 4)->nullable();
            $table->string('ensemble_method')->nullable();
            $table->string('model_version')->nullable();
            $table->json('shap_explanation')->nullable();
            $table->json('gnn_explanation')->nullable();
            $table->json('unified_explanation')->nullable();
            $table->integer('latency_ms')->nullable();
            $table->boolean('is_fraud_predicted')->default(false);
            $table->float('confidence', 8, 4)->nullable();
            $table->timestamp('scored_at')->useCurrent();
            $table->timestamps();
            
            // Indexes
            $table->unique('transaction_id');
            $table->index('risk_score');
            $table->index('is_fraud_predicted');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('ml_scores');
    }
};
