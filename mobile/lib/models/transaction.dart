class Transaction {
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
