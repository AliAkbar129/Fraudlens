import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../providers/case_provider.dart';

class CaseQueueScreen extends StatefulWidget {
  const CaseQueueScreen({super.key});

  @override
  State<CaseQueueScreen> createState() => _CaseQueueScreenState();
}

class _CaseQueueScreenState extends State<CaseQueueScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<CaseProvider>().fetchCases();
    });
  }

  @override
  Widget build(BuildContext context) {
    final cases = context.watch<CaseProvider>().cases;
    
    return Scaffold(
      appBar: AppBar(title: const Text('Case Queue')),
      body: RefreshIndicator(
        onRefresh: () => context.read<CaseProvider>().fetchCases(),
        child: ListView.builder(
          itemCount: cases.length,
          itemBuilder: (context, index) {
            final c = cases[index];
            return Card(
              child: ListTile(
                title: Text('Case ${c.id}'),
                subtitle: Text('Status: ${c.status}'),
                trailing: Text(c.priority),
                onTap: () => context.push('/cases/${c.id}'),
              ),
            );
          },
        ),
      ),
    );
  }
}
