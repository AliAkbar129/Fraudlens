<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Analyst;
use App\Http\Resources\AnalystResource;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;
use Illuminate\Support\Facades\Hash;

class AnalystController extends Controller
{
    /**
     * Display a listing of analysts.
     */
    public function index(): AnonymousResourceCollection
    {
        $analysts = Analyst::where('is_active', true)->get();
        return AnalystResource::collection($analysts);
    }

    /**
     * Display the specified analyst.
     */
    public function show($id): AnalystResource
    {
        $analyst = Analyst::findOrFail($id);
        
        $stats = [
            'open_cases_count' => $analyst->assignedCases()->open()->count(),
            'resolved_today' => $analyst->assignedCases()->whereDate('resolved_at', today())->count(),
            'avg_resolution_time' => 120, // Mocked minutes
        ];
        
        $analyst->stats = $stats;
        return new AnalystResource($analyst);
    }

    /**
     * Get current profile.
     */
    public function profile(Request $request): AnalystResource
    {
        // Mocking user for demo, normally this is $request->user()
        $user = Analyst::first(); 
        return new AnalystResource($user);
    }
    
    /**
     * Update current profile.
     */
    public function updateProfile(Request $request): AnalystResource
    {
        $user = Analyst::first(); // Mocked
        $data = $request->validate([
            'name' => 'sometimes|string',
            'password' => 'sometimes|string|min:8',
        ]);
        
        if (isset($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        }
        
        $user->update($data);
        return new AnalystResource($user);
    }
}
