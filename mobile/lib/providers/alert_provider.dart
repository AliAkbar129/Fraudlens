import 'package:flutter/foundation.dart';
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
