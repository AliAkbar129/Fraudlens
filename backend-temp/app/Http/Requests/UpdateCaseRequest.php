<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateCaseRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'status' => ['sometimes', 'string', 'in:open,assigned,under_review,escalated,resolved_fraud,resolved_legitimate,closed'],
            'priority' => ['sometimes', 'string', 'in:critical,high,medium,low'],
            'analyst_notes' => ['sometimes', 'string', 'nullable'],
        ];
    }
}
