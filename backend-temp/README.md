# FraudLens Backend

This is the backend service for FraudLens, built with Laravel 11.

## Getting Started

1. Copy `.env.example` to `.env`
2. Update the `.env` variables as needed (database, etc.)
3. Install dependencies:
   ```bash
   composer install
   ```
4. Generate key:
   ```bash
   php artisan key:generate
   ```
5. Run migrations and seeders:
   ```bash
   php artisan migrate --seed
   ```
6. Start the server:
   ```bash
   php artisan serve
   ```

## Architecture
- **Controllers**: Handle HTTP requests and responses.
- **Services**: Contain business logic (MlScoring, RulesEngine, CaseManagement).
- **Events/Broadcasting**: Real-time websocket events for the frontend.
- **Models**: Eloquent models with appropriate scopes and relationships.
