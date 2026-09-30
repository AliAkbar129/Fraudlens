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
        Schema::create('audit_logs', function (Blueprint $table) {
            $table->id();
            $table->foreignId('case_id')->constrained('fraud_cases')->onDelete('cascade');
            $table->foreignId('analyst_id')->nullable()->constrained('analysts')->onDelete('set null');
            $table->enum('action', ['created', 'assigned', 'status_changed', 'note_added', 'escalated', 'resolved', 'reopened']);
            $table->json('previous_values')->nullable();
            $table->json('new_values')->nullable();
            $table->string('ip_address', 45)->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('audit_logs');
    }
};
