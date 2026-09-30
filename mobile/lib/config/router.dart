import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/login_screen.dart';
import '../screens/alert_feed_screen.dart';
import '../screens/transaction_detail_screen.dart';
import '../screens/case_queue_screen.dart';
import '../screens/case_detail_screen.dart';
import '../screens/settings_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/login',
  routes: [
    GoRoute(
      path: '/login',
      builder: (context, state) => const LoginScreen(),
    ),
    ShellRoute(
      builder: (context, state, child) {
        return Scaffold(
          body: child,
          bottomNavigationBar: BottomNavigationBar(
            currentIndex: _calculateSelectedIndex(state.uri.path),
            onTap: (int idx) => _onItemTapped(idx, context),
            items: const [
              BottomNavigationBarItem(icon: Icon(Icons.notifications), label: 'Alerts'),
              BottomNavigationBarItem(icon: Icon(Icons.folder), label: 'Cases'),
              BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
            ],
          ),
        );
      },
      routes: [
        GoRoute(
          path: '/home',
          builder: (context, state) => const AlertFeedScreen(),
        ),
        GoRoute(
          path: '/cases',
          builder: (context, state) => const CaseQueueScreen(),
        ),
        GoRoute(
          path: '/settings',
          builder: (context, state) => const SettingsScreen(),
        ),
      ],
    ),
    GoRoute(
      path: '/transaction/:id',
      builder: (context, state) => TransactionDetailScreen(id: state.pathParameters['id']!),
    ),
    GoRoute(
      path: '/cases/:id',
      builder: (context, state) => CaseDetailScreen(id: state.pathParameters['id']!),
    ),
  ],
);

int _calculateSelectedIndex(String location) {
  if (location.startsWith('/home')) return 0;
  if (location.startsWith('/cases')) return 1;
  if (location.startsWith('/settings')) return 2;
  return 0;
}

void _onItemTapped(int index, BuildContext context) {
  switch (index) {
    case 0:
      context.go('/home');
      break;
    case 1:
      context.go('/cases');
      break;
    case 2:
      context.go('/settings');
      break;
  }
}
