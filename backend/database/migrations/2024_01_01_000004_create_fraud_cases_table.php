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
        Schema::create('fraud_cases', function (Blueprint $table) {
            $table->id();
            $table->foreignId('transaction_id')->constrained()->onDelete('cascade');
            $table->foreignId('ml_score_id')->constrained()->onDelete('cascade');
            $table->string('case_number')->unique();
            $table->enum('status', ['open', 'assigned', 'under_review', 'escalated', 'resolved_fraud', 'resolved_legitimate', 'closed'])->default('open');
            $table->enum('priority', ['critical', 'high', 'medium', 'low'])->default('medium');
            $table->foreignId('assigned_analyst_id')->nullable()->constrained('analysts')->onDelete('set null');
            $table->text('analyst_notes')->nullable();
            $table->enum('resolution', ['confirmed_fraud', 'false_positive', 'needs_investigation', 'legitimate'])->nullable();
            $table->text('resolution_reason')->nullable();
            $table->timestamp('sla_deadline')->nullable();
            $table->timestamp('resolved_at')->nullable();
            $table->timestamps();
            
            // Indexes
            $table->index('status');
            $table->index('priority');
            $table->index('assigned_analyst_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('fraud_cases');
    }
};
