import 'dart:convert';
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
