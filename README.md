# FraudLens

![Build Status](https://img.shields.io/github/actions/workflow/status/user/fraudlens/ci.yml)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![PHP](https://img.shields.io/badge/php-8.3-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.0-blue.svg)

FraudLens is an enterprise-grade fraud detection and management platform. It uses machine learning to score transactions in real-time and provides a comprehensive dashboard and mobile app for human review.

## Architecture

```mermaid
graph LR
    A[Client App/Web] --> B[Nginx Proxy]
    B --> C[Frontend SPA]
    B --> D[Backend API PHP]
    D --> E[(MySQL)]
    D --> F[(MongoDB)]
    D --> G[(Redis)]
    D --> H[ML Service Python]
```

## Tech Stack
| Component | Technology |
|---|---|
| Frontend | Vue/React/Svelte + TypeScript |
| Backend | PHP 8.3 + Laravel |
| ML Pipeline | Python 3.11 + PyTorch/XGBoost |
| Mobile | Flutter |
| Database | MySQL + MongoDB |
| Cache/Queue | Redis |

## Prerequisites
- Docker and Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11 (for local ML dev)
- PHP 8.3 (for local backend dev)
- Flutter SDK (for mobile dev)

## Quick Start
1. Clone the repository
2. `cp docker/.env.example .env`
3. `docker compose up -d --build`

## Development
See individual READMEs in each service directory.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
