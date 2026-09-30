import 'package:flutter/material.dart';

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
