import 'package:flutter/material.dart';
import '../widgets/risk_gauge_painter.dart';

class TransactionDetailScreen extends StatelessWidget {
  final String id;
  const TransactionDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Transaction $id')),
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  SizedBox(
                    height: 200,
                    width: 200,
                    child: CustomPaint(
                      painter: RiskGaugePainter(score: 0.85),
                    ),
                  ),
                  const SizedBox(height: 20),
                  const Text('Top Features:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const ListTile(title: Text('Amount'), trailing: Text('+0.15')),
                  const ListTile(title: Text('Location'), trailing: Text('+0.10')),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.green), child: const Text('Approve')),
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.amber), child: const Text('Escalate')),
                      ElevatedButton(onPressed: (){}, style: ElevatedButton.styleFrom(backgroundColor: Colors.red), child: const Text('Flag')),
                    ],
                  )
                ],
              ),
            ),
          )
        ],
      ),
    );
  }
}
