import os

base_dir = r"C:\Users\User\.gemini\antigravity\scratch\fraudlens"

files = {
    "docker-compose.yml": """version: '3.8'

services:
  ml-service:
    build:
      context: ./ml-pipeline
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
      - API_KEY=${ML_API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - redis
    volumes:
      - model_artifacts:/app/models
    restart: unless-stopped
    networks:
      - fraudlens-network

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DB_CONNECTION=mysql
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_DATABASE=${DB_DATABASE}
      - DB_USERNAME=${DB_USERNAME}
      - DB_PASSWORD=${DB_PASSWORD}
      - MONGODB_URI=${MONGODB_URI}
      - ML_API_URL=http://ml-service:8000
      - REDIS_HOST=redis
      - APP_KEY=${APP_KEY}
      - APP_ENV=${APP_ENV:-production}
    depends_on:
      mysql:
        condition: service_healthy
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
      ml-service:
        condition: service_started
    restart: unless-stopped
    networks:
      - fraudlens-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    networks:
      - fraudlens-network

  mysql:
    image: mysql:8.0
    ports:
      - "3306:3306"
    environment:
      - MYSQL_DATABASE=${DB_DATABASE}
      - MYSQL_USER=${DB_USERNAME}
      - MYSQL_PASSWORD=${DB_PASSWORD}
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - fraudlens-network

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - fraudlens-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - redis_data:/data
    networks:
      - fraudlens-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
      - ml-service
    networks:
      - fraudlens-network

networks:
  fraudlens-network:
    driver: bridge

volumes:
  mysql_data:
  mongodb_data:
  redis_data:
  model_artifacts:
""",
    "docker/nginx/nginx.conf": """worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include mime.types;
    default_type application/octet-stream;
    
    sendfile on;
    keepalive_timeout 65;
    
    # Gzip configuration
    gzip on;
    gzip_vary on;
    gzip_min_length 10240;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml application/javascript;
    gzip_disable "MSIE [1-6]\.";
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";
    add_header Content-Security-Policy "default-src 'self'; connect-src 'self' ws: wss:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; img-src 'self' data:;";
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=10r/s;
    
    client_max_body_size 10M;
    
    # Proxy timeout
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    server {
        listen 80;
        server_name localhost;
        
        # SSL config placeholder
        # listen 443 ssl;
        # ssl_certificate /etc/nginx/ssl/cert.pem;
        # ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://frontend:80;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /api/ {
            limit_req zone=mylimit burst=20 nodelay;
            proxy_pass http://backend:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /ml/ {
            proxy_pass http://ml-service:8000/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
        
        location /ws {
            proxy_pass http://backend:8080/ws;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
""",
    "docker/.env.example": """# App Config
APP_ENV=production
APP_DEBUG=false
APP_KEY=base64:PLACEHOLDER_KEY=

# MySQL Database
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=fraudlens_db
DB_USERNAME=fraudlens_user
DB_PASSWORD=secret
DB_ROOT_PASSWORD=root_secret

# MongoDB
MONGODB_URI=mongodb://mongo_user:mongo_secret@mongodb:27017/fraudlens?authSource=admin
MONGO_INITDB_ROOT_USERNAME=mongo_user
MONGO_INITDB_ROOT_PASSWORD=mongo_secret

# Redis
REDIS_HOST=redis
REDIS_PASSWORD=null
REDIS_PORT=6379

# ML Service
ML_API_URL=http://ml-service:8000
ML_API_KEY=ml_secret_key
LOG_LEVEL=INFO

# WebSockets
PUSHER_APP_ID=placeholder_app_id
PUSHER_APP_KEY=placeholder_app_key
PUSHER_APP_SECRET=placeholder_app_secret
PUSHER_HOST=127.0.0.1
PUSHER_PORT=6001
PUSHER_SCHEME=http
""",
    "frontend/Dockerfile": """# Stage 1: Build
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""",
    "frontend/nginx.conf": """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?|eot|ttf|otf)$ {
        expires 1y;
        add_header Cache-Control "public, no-transform";
    }
}
""",
    ".github/workflows/ci.yml": """name: FraudLens CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-test-python:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./ml-pipeline
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8 mypy
      - name: Lint with flake8
        run: flake8 .
      - name: Type check with mypy
        run: mypy .
      - name: Test with pytest
        run: pytest --cov=./ --cov-report=xml

  lint-and-test-php:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./backend
    steps:
      - uses: actions/checkout@v3
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.3'
          tools: composer
      - name: Get Composer Cache Directory
        id: composer-cache
        run: |
          echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT
      - uses: actions/cache@v3
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: |
            ${{ runner.os }}-composer-
      - name: Install dependencies
        run: composer install --prefer-dist --no-progress
      - name: Run PHPStan
        run: vendor/bin/phpstan analyse
      - name: Run PHPUnit
        run: vendor/bin/phpunit

  lint-and-test-frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./frontend
    steps:
      - uses: actions/checkout@v3
      - name: Use Node.js 20
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: './frontend/package-lock.json'
      - name: Install dependencies
        run: npm ci
      - name: Lint
        run: npm run lint
      - name: Type check
        run: npx tsc --noEmit
      - name: Test
        run: npm run test:unit
      - name: Build
        run: npm run build

  docker-build:
    needs: [lint-and-test-python, lint-and-test-php, lint-and-test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and Start containers
        run: |
          cp docker/.env.example .env
          docker compose up -d --build
      - name: Check running containers
        run: docker compose ps
      - name: Wait for services
        run: sleep 30
      - name: Check logs if anything failed
        run: docker compose logs
""",
    ".gitignore": """# OS
.DS_Store
Thumbs.db
*.swp

# IDEs
.idea/
.vscode/
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Environment
.env
!.env.example
.env.*
!.env.*.example

# Logs and databases
*.log
*.sqlite
*.db

# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
env/
venv/
ENV/
env.bak/
venv.bak/
.eggs/
*.egg-info/
*.egg
dist/
build/
.pytest_cache/
.coverage
coverage.xml
htmlcov/
.mypy_cache/

# PHP
vendor/
node_modules/
public/hot
public/storage
storage/*.key
storage/framework/cache/data/
storage/framework/sessions/
storage/framework/testing/
storage/framework/views/
storage/logs/

# Node/Frontend
node_modules/
dist/
dist-ssr/
*.local
.npm
coverage/
.vite/

# Docker
volumes/
mysql_data/
mongodb_data/
redis_data/

# Model Artifacts
ml-pipeline/models/*.pt
ml-pipeline/models/*.pkl
ml-pipeline/models/*.joblib
!ml-pipeline/models/.gitkeep

# Flutter / Mobile
mobile/.dart_tool/
mobile/.packages
mobile/build/
mobile/.flutter-plugins
mobile/.flutter-plugins-dependencies
mobile/android/local.properties
mobile/ios/Flutter/App.framework
mobile/ios/Flutter/Flutter.framework
mobile/ios/Flutter/Generated.xcconfig
mobile/ios/Flutter/app.flx
mobile/ios/Flutter/flutter_assets/
mobile/ios/Flutter/flutter_export_environment.sh
""",
    "README.md": """# FraudLens

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
""",
    "mobile/pubspec.yaml": """name: fraudlens
description: FraudLens mobile app.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  firebase_core: ^2.14.0
  firebase_messaging: ^14.6.4
  firebase_auth: ^4.6.3
  http: ^1.1.0
  fl_chart: ^0.63.0
  provider: ^6.0.5
  go_router: ^10.0.0
  shared_preferences: ^2.2.0
  intl: ^0.18.1
  google_fonts: ^5.1.0
  flutter_animate: ^4.2.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.0

flutter:
  uses-material-design: true
""",
    "mobile/lib/main.dart": """import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
// import 'package:firebase_core/firebase_core.dart';
import 'config/theme.dart';
import 'config/router.dart';
import 'providers/auth_provider.dart';
import 'providers/alert_provider.dart';
import 'providers/case_provider.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // await Firebase.initializeApp();
  runApp(const FraudLensApp());
}

class FraudLensApp extends StatelessWidget {
  const FraudLensApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => AlertProvider()),
        ChangeNotifierProvider(create: (_) => CaseProvider()),
      ],
      child: MaterialApp.router(
        title: 'FraudLens',
        theme: AppTheme.darkTheme,
        routerConfig: appRouter,
        debugShowCheckedModeBanner: false,
      ),
    );
  }
}
""",
    "mobile/lib/config/theme.dart": """import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const Color background = Color(0xFF0A0A0F);
  static const Color primary = Color(0xFF00D4FF);
  static const Color success = Color(0xFF00FF88);
  static const Color danger = Color(0xFFFF3366);
  static const Color warning = Color(0xFFFFC107);
  static const Color cardColor = Color(0xFF15151E);
  static const Color textMain = Colors.white;
  static const Color textSub = Colors.white70;

  static ThemeData get darkTheme {
    return ThemeData(
      brightness: Brightness.dark,
      scaffoldBackgroundColor: background,
      primaryColor: primary,
      cardColor: cardColor,
      textTheme: GoogleFonts.interTextTheme(
        ThemeData.dark().textTheme,
      ),
      colorScheme: const ColorScheme.dark(
        primary: primary,
        secondary: success,
        error: danger,
        background: background,
        surface: cardColor,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }
}
""",
    "mobile/lib/config/router.dart": """import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/login_screen.dart';
import '../screens/alert_feed_screen.dart';
import '../screens/transaction_detail_screen.dart';
import '../screens/case_queue_screen.dart';
import '../screens/case_detail_screen.dart';
import '../screens/settings_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    ShellRoute(
      builder: (context, state, child) {
        return Scaffold(
          body: child,
          bottomNavigationBar: BottomNavigationBar(
            currentIndex: _calculateSelectedIndex(state.uri.path),
            onTap: (int idx) => _onItemTapped(idx, context),
            items: const [
              BottomNavigationBarItem(icon: Icon(Icons.notifications), label: 'Alerts'),
              BottomNavigationBarItem(icon: Icon(Icons.folder), label: 'Cases'),
              BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
            ],
          ),
        );
      },
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const AlertFeedScreen(),
        ),
        GoRoute(
          path: '/cases',
          builder: (context, state) => const CaseQueueScreen(),
        ),
        GoRoute(
          path: '/settings',
          builder: (context, state) => const SettingsScreen(),
        ),
      ],
    ),
    GoRoute(
      path: '/transaction/:id',
      builder: (context, state) => TransactionDetailScreen(id: state.pathParameters['id']!),
    ),
    GoRoute(
      path: '/cases/:id',
      builder: (context, state) => CaseDetailScreen(id: state.pathParameters['id']!),
    ),
  ],
);

int _calculateSelectedIndex(String location) {
  if (location.startsWith('/home')) return 0;
  if (location.startsWith('/cases')) return 1;
  if (location.startsWith('/settings')) return 2;
  return 0;
}

void _onItemTapped(int index, BuildContext context) {
  switch (index) {
    case 0:
      context.go('/home');
      break;
    case 1:
      context.go('/cases');
      break;
    case 2:
      context.go('/settings');
      break;
  }
}
""",
    "mobile/lib/models/transaction.dart": """class Transaction {
  final String id;
  final double amount;
  final String type;
  final String channel;
  final DateTime timestamp;

  Transaction({
    required this.id,
    required this.amount,
    required this.type,
    required this.channel,
    required this.timestamp,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) {
    return Transaction(
      id: json['id'],
      amount: json['amount'].toDouble(),
      type: json['type'],
      channel: json['channel'],
      timestamp: DateTime.parse(json['timestamp']),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'amount': amount,
    'type': type,
    'channel': channel,
    'timestamp': timestamp.toIso8601String(),
  };
}
""",
    "mobile/lib/models/ml_score.dart": """class MlScore {
  final String transactionId;
  final double riskScore;
  final List<String> topFeatures;

  MlScore({
    required this.transactionId,
    required this.riskScore,
    required this.topFeatures,
  });

  factory MlScore.fromJson(Map<String, dynamic> json) {
    return MlScore(
      transactionId: json['transactionId'],
      riskScore: json['riskScore'].toDouble(),
      topFeatures: List<String>.from(json['topFeatures']),
    );
  }
}
""",
    "mobile/lib/models/fraud_case.dart": """class FraudCase {
  final String id;
  final String transactionId;
  final String status;
  final String priority;
  final DateTime createdAt;

  FraudCase({
    required this.id,
    required this.transactionId,
    required this.status,
    required this.priority,
    required this.createdAt,
  });

  factory FraudCase.fromJson(Map<String, dynamic> json) {
    return FraudCase(
      id: json['id'],
      transactionId: json['transactionId'],
      status: json['status'],
      priority: json['priority'],
      createdAt: DateTime.parse(json['createdAt']),
    );
  }
}
""",
    "mobile/lib/models/alert.dart": """class Alert {
  final String id;
  final String title;
  final String message;
  final double riskScore;
  final String transactionRef;
  bool isRead;
  final DateTime createdAt;

  Alert({
    required this.id,
    required this.title,
    required this.message,
    required this.riskScore,
    required this.transactionRef,
    this.isRead = false,
    required this.createdAt,
  });

  factory Alert.fromJson(Map<String, dynamic> json) {
    return Alert(
      id: json['id'],
      title: json['title'],
      message: json['message'],
      riskScore: json['risk_score'].toDouble(),
      transactionRef: json['transaction_ref'],
      isRead: json['is_read'] ?? false,
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}
""",
    "mobile/lib/services/api_service.dart": """import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/alert.dart';
import '../models/transaction.dart';
import '../models/fraud_case.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8080/api';
  String? token;

  Future<void> login(String email, String password) async {
    // Implement API login
    token = "fake-token";
  }

  Future<List<Alert>> getAlerts() async {
    // Return mock data for now
    return [
      Alert(id: '1', title: 'High Risk Transfer', message: 'Unusual amount detected', riskScore: 0.95, transactionRef: 'tx-101', createdAt: DateTime.now()),
    ];
  }

  Future<Transaction> getTransaction(String id) async {
    return Transaction(id: id, amount: 5000, type: 'WIRE', channel: 'WEB', timestamp: DateTime.now());
  }

  Future<List<FraudCase>> getCases() async {
    return [
      FraudCase(id: 'c-1', transactionId: 'tx-101', status: 'OPEN', priority: 'HIGH', createdAt: DateTime.now()),
    ];
  }

  Future<FraudCase> getCase(String id) async {
    return FraudCase(id: id, transactionId: 'tx-101', status: 'OPEN', priority: 'HIGH', createdAt: DateTime.now());
  }

  Future<void> updateCase(String id, String status) async {}
  Future<void> resolveCase(String id) async {}
}
""",
    "mobile/lib/services/notification_service.dart": """class NotificationService {
  void init() {
    // FirebaseMessaging.instance.requestPermission();
  }
}
""",
    "mobile/lib/services/auth_service.dart": """class AuthService {
  Future<bool> signIn(String email, String password) async {
    return true;
  }
  void signOut() {}
}
""",
    "mobile/lib/providers/auth_provider.dart": """import 'package:flutter/foundation.dart';

class AuthProvider extends ChangeNotifier {
  bool _isAuthenticated = false;
  bool get isAuthenticated => _isAuthenticated;

  Future<void> login(String email, String password) async {
    _isAuthenticated = true;
    notifyListeners();
  }

  void logout() {
    _isAuthenticated = false;
    notifyListeners();
  }
}
""",
    "mobile/lib/providers/alert_provider.dart": """import 'package:flutter/foundation.dart';
import '../models/alert.dart';

class AlertProvider extends ChangeNotifier {
  List<Alert> _alerts = [];
  List<Alert> get alerts => _alerts;

  int get unreadCount => _alerts.where((a) => !a.isRead).length;

  Future<void> fetchAlerts() async {
    _alerts = [
      Alert(id: '1', title: 'Suspicious Login', message: 'Login from new IP', riskScore: 0.8, transactionRef: 'tx-001', createdAt: DateTime.now()),
    ];
    notifyListeners();
  }

  void markAsRead(String id) {
    final index = _alerts.indexWhere((a) => a.id == id);
    if (index != -1) {
      _alerts[index].isRead = true;
      notifyListeners();
    }
  }
}
""",
    "mobile/lib/providers/case_provider.dart": """import 'package:flutter/foundation.dart';
import '../models/fraud_case.dart';

class CaseProvider extends ChangeNotifier {
  List<FraudCase> _cases = [];
  List<FraudCase> get cases => _cases;

  Future<void> fetchCases() async {
    _cases = [
      FraudCase(id: 'c-1', transactionId: 'tx-101', status: 'OPEN', priority: 'HIGH', createdAt: DateTime.now()),
    ];
    notifyListeners();
  }
}
""",
    "mobile/lib/screens/login_screen.dart": """import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../providers/auth_provider.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.security, size: 80, color: Color(0xFF00D4FF)),
              const SizedBox(height: 16),
              const Text('FraudLens', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
              const SizedBox(height: 48),
              TextField(decoration: const InputDecoration(labelText: 'Email', border: OutlineInputBorder())),
              const SizedBox(height: 16),
              TextField(obscureText: true, decoration: const InputDecoration(labelText: 'Password', border: OutlineInputBorder())),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () async {
                  await context.read<AuthProvider>().login('email', 'password');
                  context.go('/home');
                },
                child: const Text('Login'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
""",
    "mobile/lib/screens/alert_feed_screen.dart": """import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../providers/alert_provider.dart';

class AlertFeedScreen extends StatefulWidget {
  const AlertFeedScreen({super.key});

  @override
  State<AlertFeedScreen> createState() => _AlertFeedScreenState();
}

class _AlertFeedScreenState extends State<AlertFeedScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AlertProvider>().fetchAlerts();
    });
  }

  @override
  Widget build(BuildContext context) {
    final alerts = context.watch<AlertProvider>().alerts;
    
    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: alerts.isEmpty ? const Center(child: Text('All clear')) : RefreshIndicator(
        onRefresh: () => context.read<AlertProvider>().fetchAlerts(),
        child: ListView.builder(
          itemCount: alerts.length,
          itemBuilder: (context, index) {
            final alert = alerts[index];
            return Dismissible(
              key: Key(alert.id),
              onDismissed: (_) => context.read<AlertProvider>().markAsRead(alert.id),
              child: Card(
                child: ListTile(
                  title: Text(alert.title),
                  subtitle: Text(alert.message),
                  trailing: Text(alert.riskScore.toString()),
                  onTap: () => context.push('/transaction/\${alert.transactionRef}'),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
""",
    "mobile/lib/screens/transaction_detail_screen.dart": """import 'package:flutter/material.dart';
import '../widgets/risk_gauge_painter.dart';

class TransactionDetailScreen extends StatelessWidget {
  final String id;
  const TransactionDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Transaction \$id')),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  SizedBox(
                    height: 200,
                    width: 200,
                    child: CustomPaint(
                      painter: RiskGaugePainter(score: 0.85),
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text('Top Features:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const ListTile(title: Text('Amount'), trailing: Text('+0.15')),
                  const ListTile(title: Text('Location'), trailing: Text('+0.10')),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.green), child: const Text('Approve')),
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.amber), child: const Text('Escalate')),
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.red), child: const Text('Flag')),
                    ],
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
""",
    "mobile/lib/screens/case_queue_screen.dart": """import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../providers/case_provider.dart';

class CaseQueueScreen extends StatefulWidget {
  const CaseQueueScreen({super.key});

  @override
  State<CaseQueueScreen> createState() => _CaseQueueScreenState();
}

class _CaseQueueScreenState extends State<CaseQueueScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CaseProvider>().fetchCases();
    });
  }

  @override
  Widget build(BuildContext context) {
    final cases = context.watch<CaseProvider>().cases;
    
    return Scaffold(
      appBar: AppBar(title: const Text('Case Queue')),
      body: RefreshIndicator(
        onRefresh: () => context.read<CaseProvider>().fetchCases(),
        child: ListView.builder(
          itemCount: cases.length,
          itemBuilder: (context, index) {
            final c = cases[index];
            return Card(
              child: ListTile(
                title: Text('Case \${c.id}'),
                subtitle: Text('Status: \${c.status}'),
                trailing: Text(c.priority),
                onTap: () => context.push('/cases/\${c.id}'),
              ),
            );
          },
        ),
      ),
    );
  }
}
""",
    "mobile/lib/screens/case_detail_screen.dart": """import 'package:flutter/material.dart';

class CaseDetailScreen extends StatelessWidget {
  final String id;
  const CaseDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Case \$id')),
      body: Center(child: Text('Case Details for \$id')),
    );
  }
}
""",
    "mobile/lib/screens/settings_screen.dart": """import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../providers/auth_provider.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          const ListTile(title: Text('Notifications'), trailing: Switch(value: true, onChanged: null)),
          const ListTile(title: Text('Dark Theme'), trailing: Switch(value: true, onChanged: null)),
          ListTile(
            title: const Text('Logout', style: TextStyle(color: Colors.red)),
            onTap: () {
              context.read<AuthProvider>().logout();
              context.go('/login');
            },
          )
        ],
      ),
    );
  }
}
""",
    "mobile/lib/widgets/risk_gauge_painter.dart": """import 'package:flutter/material.dart';
import 'dart:math';

class RiskGaugePainter extends CustomPainter {
  final double score;

  RiskGaugePainter({required this.score});

  @override
  void paint(Canvas canvas, Size size) {
    Paint paint = Paint()
      ..color = Colors.grey.withOpacity(0.2)
      ..strokeWidth = 15
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    Offset center = Offset(size.width / 2, size.height / 2);
    double radius = min(size.width / 2, size.height / 2) - 15;

    canvas.drawArc(Rect.fromCircle(center: center, radius: radius), pi, pi, false, paint);

    Paint scorePaint = Paint()
      ..color = _getColor()
      ..strokeWidth = 15
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(Rect.fromCircle(center: center, radius: radius), pi, pi * score, false, scorePaint);
  }
  
  Color _getColor() {
    if (score < 0.3) return Colors.green;
    if (score < 0.7) return Colors.orange;
    return Colors.red;
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
""",
    "mobile/lib/widgets/status_badge.dart": """import 'package:flutter/material.dart';

class StatusBadge extends StatelessWidget {
  final String text;
  final Color color;

  const StatusBadge({super.key, required this.text, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.2),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color),
      ),
      child: Text(text, style: TextStyle(color: color, fontSize: 12)),
    );
  }
}
""",
    "mobile/lib/widgets/shap_feature_bar.dart": """import 'package:flutter/material.dart';

class ShapFeatureBar extends StatelessWidget {
  final String feature;
  final double value;

  const ShapFeatureBar({super.key, required this.feature, required this.value});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        children: [
          Expanded(flex: 2, child: Text(feature, overflow: TextOverflow.ellipsis)),
          Expanded(
            flex: 3,
            child: LinearProgressIndicator(
              value: value.abs(),
              color: value > 0 ? Colors.red : Colors.green,
              backgroundColor: Colors.grey[800],
            ),
          )
        ],
      ),
    );
  }
}
""",
    "mobile/lib/widgets/glass_card.dart": """import 'package:flutter/material.dart';
import 'dart:ui';

class GlassCard extends StatelessWidget {
  final Widget child;

  const GlassCard({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(16),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
        child: Container(
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withOpacity(0.1)),
          ),
          child: child,
        ),
      ),
    );
  }
}
""",
    "mobile/lib/widgets/animated_counter.dart": """import 'package:flutter/material.dart';

class AnimatedCounter extends StatelessWidget {
  final int count;

  const AnimatedCounter({super.key, required this.count});

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder(
      tween: IntTween(begin: 0, end: count),
      duration: const Duration(seconds: 1),
      builder: (context, value, child) {
        return Text(value.toString(), style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold));
      },
    );
  }
}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Created {len(files)} files successfully.")
