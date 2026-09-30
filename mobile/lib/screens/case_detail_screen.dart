import 'package:flutter/material.dart';

class CaseDetailScreen extends StatelessWidget {
  final String id;
  const CaseDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Case $id')),
      body: Center(child: Text('Case Details for $id')),
    );
  }
}
