import 'package:flutter/material.dart';
import 'package:ai_assistant/theme/project_colors.dart';
import 'package:ai_assistant/services/stream_web_search_service.dart';
import 'package:skeletonizer/skeletonizer.dart';

class SourcesSection extends StatefulWidget {
  const SourcesSection({super.key});

  @override
  State<SourcesSection> createState() => _SourcesSectionState();
}

class _SourcesSectionState extends State<SourcesSection> {
  bool isLoading = true;
  List searchResults = [
  {
    'title': 'E.T. the Extra-Terrestrial - IMDb',
    'url': 'https://www.imdb.com/title/tt0083866/',
  },
  {
    'title': 'E.T. the Extra-Terrestrial - Wikipedia',
    'url': 'https://en.wikipedia.org/wiki/E.T._the_Extra-Terrestrial',
  },
  {
    'title': 'Watch E.T. on Universal Pictures',
    'url': 'https://www.uphe.com/movies/et-the-extra-terrestrial',
  },
  ];

  @override
  void initState() {
    super.initState();
    StreamWebService().searchResultStream.listen((data) {
      setState(() {
        searchResults = data['data'];
        isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Skeletonizer(
      enabled: isLoading,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: searchResults.map((res) {
          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: ProjectColors.cardColor,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(res['title'], style: TextStyle(fontWeight: FontWeight.w500), maxLines: 2, overflow: TextOverflow.ellipsis,),
                  const SizedBox(height: 8,),
                  Text(res['url'], style: TextStyle(color: Colors.grey, fontSize: 12), maxLines: 1, overflow: TextOverflow.ellipsis,)
                ],
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}