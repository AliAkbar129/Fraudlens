<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class IngestTransactionRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true; // Authentication handled by middleware
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'transaction_ref' => ['required', 'string', 'max:64', 'unique:transactions'],
            'amount' => ['required', 'numeric', 'min:0'],
            'currency' => ['nullable', 'string', 'size:3'],
            'type' => ['required', 'string', 'in:purchase,transfer,withdrawal,deposit,bill_payment,top_up'],
            'channel' => ['required', 'string', 'in:web,mobile_app,pos,atm,agent'],
            'sender_account' => ['nullable', 'string'],
            'receiver_account' => ['nullable', 'string'],
            'merchant_category' => ['nullable', 'string'],
            'device_info' => ['nullable', 'string'],
            'ip_address' => ['nullable', 'ip'],
            'email' => ['nullable', 'email'],
            'card_hash' => ['nullable', 'string', 'max:64'],
            'raw_features' => ['nullable', 'array'],
            'occurred_at' => ['required', 'date'],
        ];
    }
}
