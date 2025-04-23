import 'package:ai_assistant/widgets/ai_summary.dart';
import 'package:ai_assistant/widgets/main_search_bar.dart';
import 'package:ai_assistant/widgets/sources.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int tapCount = 0;

  void _handleSearchTap() {
    setState(() {
      tapCount++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          const SizedBox(width: 200,),
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 25,),
                  MainSearchBar(onSearchTapped: _handleSearchTap,),
                  const SizedBox(height: 25),
                  if (tapCount > 0)
                    Column(
                      children: [
                        AiSummary(),
                        const SizedBox(height: 20,),
                        SourcesSection()
                      ],
                    ),
                ],
              ),
            ),
          ),
          const SizedBox(width: 200,),
        ],
      ),
    );
  }
}