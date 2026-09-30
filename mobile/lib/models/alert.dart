class Alert {
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
