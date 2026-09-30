<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreRuleRequest extends FormRequest
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
            'name' => ['required', 'string', 'max:255'],
            'description' => ['nullable', 'string'],
            'conditions' => ['required', 'array', 'min:1'],
            'conditions.*.field' => ['required', 'string'],
            'conditions.*.operator' => ['required', 'string', 'in:>,<,>=,<=,==,!=,in,not_in,contains,between'],
            'conditions.*.value' => ['required'],
            'action' => ['required', 'string', 'in:auto_flag,auto_escalate,auto_block,notify,require_review'],
            'priority' => ['required', 'integer'],
            'is_active' => ['boolean'],
        ];
    }
}
