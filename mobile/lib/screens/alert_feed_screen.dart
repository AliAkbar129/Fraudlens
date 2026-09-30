import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:go_router/go_router.dart';
import '../providers/alert_provider.dart';

class AlertFeedScreen extends StatefulWidget {
  const AlertFeedScreen({super.key});

  @override
  State<AlertFeedScreen> createState() => _AlertFeedScreenState();
}

class _AlertFeedScreenState extends State<AlertFeedScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<AlertProvider>().fetchAlerts();
    });
  }

  @override
  Widget build(BuildContext context) {
    final alerts = context.watch<AlertProvider>().alerts;
    
    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: alerts.isEmpty ? const Center(child: Text('All clear')) : RefreshIndicator(
        onRefresh: () => context.read<AlertProvider>().fetchAlerts(),
        child: ListView.builder(
          itemCount: alerts.length,
          itemBuilder: (context, index) {
            final alert = alerts[index];
            return Dismissible(
              key: Key(alert.id),
              onDismissed: (_) => context.read<AlertProvider>().markAsRead(alert.id),
              child: Card(
                child: ListTile(
                  title: Text(alert.title),
                  subtitle: Text(alert.message),
                  trailing: Text(alert.riskScore.toString()),
                  onTap: () => context.push('/transaction/${alert.transactionRef}'),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
