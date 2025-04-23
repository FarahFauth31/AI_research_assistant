import 'dart:async';
import 'package:web_socket_client/web_socket_client.dart';
import 'dart:convert';

class StreamWebService {
  static final _instance = StreamWebService._internal(); //Making sure that only one class of StreamWebService exists (singleton pattern)
  WebSocket? _socket;

  factory StreamWebService() => _instance; //When the StreamWebService class is instantiated, the same instance is returned

  StreamWebService._internal(); //Privatized constructor
  final _searchResultController = StreamController<Map<String, dynamic>>();
  final _contentController = StreamController<Map<String, dynamic>>();
  Stream<Map<String, dynamic>> get searchResultStream => _searchResultController.stream;
  Stream<Map<String, dynamic>> get contentStream => _contentController.stream;

  //Listen to data sent to/from server
  void connect() {
    _socket = WebSocket(Uri.parse("ws://localhost:8000/ws/search-query"));
    _socket!.messages.listen((message) {
      final data = json.decode(message);
      if (data['type'] == 'search_result') {
        _searchResultController.add(data);
      } else if (data['type'] == 'content') {
        _contentController.add(data);
      }
    });
  }

  //Send data to server
  void chat(String query) {
    _socket!.send(json.encode({'query': query}));
  }
}