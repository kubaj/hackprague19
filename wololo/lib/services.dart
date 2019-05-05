import 'dart:io';

import 'package:wololo/post_model_basic.dart';
import 'package:http/http.dart' as http;

String endpointUrl = 'apigo-6um4xsxxgq-uc.a.run.app';

Future<Post> getPost() async{
  final response = await http.get('$endpointUrl');
  return postFromJson(response.body);
}

//Future<http.Response> createPost(Post post) async{
//  final response = await http.get('$endpointUrl',
//    headers: {
//      HttpHeaders.contentTypeHeader: 'application/json'
//    },
////    body: postToJson(post)
//  );
//  return response;
//}

Future<Post> createPost(String param) async{
  var queryParams = {
    'address': param,
  };
  var uri = Uri.https(endpointUrl, '/', queryParams);
  print(uri.toString());
  final response = await http.get(uri,
    headers: {
      HttpHeaders.contentTypeHeader: 'application/json'
    },
//    body: postToJson(post)
  );
  return postFromJson(response.body);
}
