import 'package:flutter/material.dart';
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
