class FraudCase {
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
