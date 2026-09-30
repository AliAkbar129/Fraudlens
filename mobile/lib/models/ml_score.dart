class MlScore {
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
