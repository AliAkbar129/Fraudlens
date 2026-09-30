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
        Schema::create('transactions', function (Blueprint $table) {
            $table->id();
            $table->string('transaction_ref', 64)->unique();
            $table->decimal('amount', 15, 2);
            $table->string('currency', 3)->default('PKR');
            $table->enum('type', ['purchase', 'transfer', 'withdrawal', 'deposit', 'bill_payment', 'top_up']);
            $table->enum('channel', ['web', 'mobile_app', 'pos', 'atm', 'agent']);
            $table->string('sender_account')->nullable();
            $table->string('receiver_account')->nullable();
            $table->string('merchant_category')->nullable();
            $table->text('device_info')->nullable();
            $table->string('ip_address', 45)->nullable();
            $table->string('email')->nullable();
            $table->string('card_hash', 64)->nullable();
            $table->json('raw_features')->nullable();
            $table->timestamp('occurred_at');
            $table->timestamps();
            
            // Indexes
            $table->index('card_hash');
            $table->index('ip_address');
            $table->index('email');
            $table->index('occurred_at');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('transactions');
    }
};
