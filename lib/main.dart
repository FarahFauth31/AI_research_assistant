import 'package:flutter/material.dart';
import 'package:ai_assistant/pages/home_page.dart';
import 'package:ai_assistant/theme/project_colors.dart';
import 'package:google_fonts/google_fonts.dart';
import 'services/stream_web_search_service.dart';

void main() {
  runApp(const MainApp());
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  @override
  void initState() {
    super.initState();
    StreamWebService().connect();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AI Research Assistant',
      theme: ThemeData(
        scaffoldBackgroundColor: ProjectColors.background,
        colorScheme: ColorScheme.fromSeed(seedColor: ProjectColors.footerGrey),
        textTheme: GoogleFonts.interTextTheme(
          ThemeData.dark().textTheme,
        )
      ),
      home: HomePage(),
    );
  }
}
