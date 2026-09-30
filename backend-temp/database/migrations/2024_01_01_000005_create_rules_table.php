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
        Schema::create('rules', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->text('description')->nullable();
            $table->json('conditions');
            $table->enum('action', ['auto_flag', 'auto_escalate', 'auto_block', 'notify', 'require_review']);
            $table->integer('priority')->default(0);
            $table->boolean('is_active')->default(true);
            $table->integer('hit_count')->default(0);
            $table->timestamp('last_triggered_at')->nullable();
            $table->foreignId('created_by')->constrained('analysts')->onDelete('cascade');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('rules');
    }
};
