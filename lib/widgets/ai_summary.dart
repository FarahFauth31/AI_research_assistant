import 'package:flutter/material.dart';
import 'package:skeletonizer/skeletonizer.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:ai_assistant/services/stream_web_search_service.dart';

class AiSummary extends StatefulWidget {
  const AiSummary({super.key});

  @override
  State<AiSummary> createState() => _AiSummaryState();
}

class _AiSummaryState extends State<AiSummary> {
  bool isLoading = true;
  String fullResponse = """
## E.T. the Extra-Terrestrial 👽

**E.T. the Extra-Terrestrial** is a 1982 science fiction film directed by *Steven Spielberg*. It tells the heartwarming story of a gentle alien stranded on Earth and his friendship with a young boy named Elliott. As the two form a deep bond, they work together to help E.T. return home, all while evading government agents.

The film is celebrated for its emotional depth, iconic imagery (like the flying bike scene 🌕🚲), and memorable line:  
**"E.T. phone home."**

It remains one of the most beloved and influential movies in cinematic history.
""";

  @override
  void initState() {
    super.initState();
    StreamWebService().contentStream.listen((data) {
      if(isLoading) {
        fullResponse = "";
      }
      setState(() {
        fullResponse += data['data'];
        isLoading = false;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('AI Summary', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),),
        Skeletonizer(enabled: isLoading, child: Markdown(data: fullResponse, shrinkWrap: true,)),
      ],
    );
  }
}