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
    try {
      _socket = WebSocket(Uri.parse("ws://localhost:8000/ws/search-query"));
      _socket!.messages.listen((message) {
        try {
          final data = json.decode(message);
          if (data['type'] == 'search_result') {
            _searchResultController.add(data);
          } else if (data['type'] == 'content') {
            _contentController.add(data);
          } else {
            print("Unknown message type: ${data['type']}");
          }
        } catch (e) {
          print("Error decoding message: $e");
        }
      });
    } catch (e) {
      print("Failed to connect to WebSocket: $e");
    }
  }

  //Send data to server
  void chat(String query) {
    if (_socket != null) {
      try {
        _socket!.send(json.encode({'query': query}));
      } catch (e) {
        print("Failed to send message: $e");
      }
    } else {
      print("WebSocket is not connected. Message not sent.");
    }
  }
}