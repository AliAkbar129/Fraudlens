import 'package:flutter/material.dart';

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
