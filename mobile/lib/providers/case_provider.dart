import 'package:flutter/foundation.dart';
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
