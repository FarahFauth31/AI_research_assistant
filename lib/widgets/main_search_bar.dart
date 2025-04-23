import 'package:ai_assistant/theme/project_colors.dart';
import 'package:flutter/material.dart';
import 'package:ai_assistant/services/stream_web_search_service.dart';

class MainSearchBar extends StatefulWidget {
  final VoidCallback onSearchTapped;

  const MainSearchBar({
    required this.onSearchTapped,
    super.key
  });

  @override
  State<MainSearchBar> createState() => _MainSearchBarState();
}

class _MainSearchBarState extends State<MainSearchBar> {
  final queryController = TextEditingController();

  @override
  void dispose() {
    super.dispose();
    queryController.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(10),
      width: 600,
      height: 50,
      decoration: BoxDecoration(
        color: ProjectColors.searchBar,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: ProjectColors.searchBarBorder,
          width: 0.5,
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              onSubmitted: (_) => widget.onSearchTapped(),
              controller: queryController,
              decoration: InputDecoration(
                hintText: "Search anything...",
                hintStyle: TextStyle(color: ProjectColors.textColor, fontSize: 16),
                border: InputBorder.none,
                isDense: true,
                contentPadding: EdgeInsets.zero,
              ),
            ),
          ),
          GestureDetector(
            onTap: () {
              StreamWebService().chat(queryController.text.trim());
              widget.onSearchTapped();
            },
            child: Icon(Icons.search, color: ProjectColors.searchIconColor, size: 25,),
          )
        ],
      )
    );
  }
}