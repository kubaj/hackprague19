// This example shows a [Scaffold] with an [AppBar], a [BottomAppBar] and a
// [FloatingActionButton]. The [body] is a [Text] placed in a [Center] in order
// to center the text within the [Scaffold] and the [FloatingActionButton] is
// centered and docked within the [BottomAppBar] using
// [FloatingActionButtonLocation.centerDocked]. The [FloatingActionButton] is
// connected to a callback that increments a counter.

import 'package:flutter/material.dart';
import 'package:wololo/detail_list.dart';
import 'package:wololo/post_model_basic.dart';
import 'package:wololo/services.dart';
import 'package:percent_indicator/percent_indicator.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  final Future<Post> post;

  MyApp({Key key, this.post}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Code Sample for material.Scaffold',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyStatefulWidget(),
    );
  }
}

class MyStatefulWidget extends StatefulWidget {
  MyStatefulWidget({Key key}) : super(key: key);

  @override
  _MyStatefulWidgetState createState() => _MyStatefulWidgetState();
}

class _MyStatefulWidgetState extends State<MyStatefulWidget> {
  Future<Post> post;
  TextEditingController placeController = TextEditingController();
  bool _validate = false;

  Widget build(BuildContext context) {
    return Scaffold(
        resizeToAvoidBottomPadding: false,

//      appBar: AppBar(
//        title: Text('Sample Code'),
//      ),
        body: SafeArea(
            child: Center(
                child: Column(
      children: <Widget>[
        Padding(
          padding: EdgeInsets.all(10),
          child: TextField(
            controller: placeController,
            style: TextStyle(
              fontSize: 20,
            ),
            decoration: InputDecoration(
                hintText: 'Search city',
                fillColor: Colors.blueGrey,
                errorText: _validate ? 'Search bar can\'t be empty' : null,
                border: new OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30.0),
                ),
                contentPadding: EdgeInsets.all(12)),
          ),
        ),
        Center(
          child: RaisedButton(
            child: Text('Search'),
            onPressed: () {
              setState(() {
                placeController.text.isEmpty
                    ? _validate = true
                    : _validate = false;
                if (!_validate) {
                  post = createPost(placeController.text);
                }
              });
            },
            color: Theme.of(context).accentColor,
            splashColor: Colors.blueGrey,
          ),
        ),
        FutureBuilder<Post>(
          future: post,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              if (snapshot.hasError) {
                return ErrorWidget(snapshot.error);
              }

              return ListView(
                shrinkWrap: true,
                padding: const EdgeInsets.all(20.0),
                children: snapshot.data.details.map((detail) => WololoWidget(detail)).toList(),
//                children: <Widget>[
//                  const Text('I\'m dedicating every day to you'),
//                  const Text('Domestic life was never quite my style'),
//                  const Text('When you smile, you knock me out, I fall apart'),
//                  const Text('And I thought I was so smart'),
//                ],
              );
//                return Text('${snapshot.data.name}');
//              return Center(
//                child: Column(
//                  mainAxisAlignment: MainAxisAlignment.center,
//                  children: <Widget>[
//                    LinearPercentIndicator(
//                      alignment: MainAxisAlignment.center,
//                      width: 200,
//                      trailing: Icon(Icons.insert_emoticon),
//                      lineHeight: 20,
//                      percent: snapshot.data.quality / 10,
//                      progressColor: setProgressColor(snapshot.data.quality),
//                      animationDuration: 250,
//                      animation: true,
//                    ),
//                    Text(
////                        snapshot.data.name
//                        'aa'),
//                    Expanded(
//                      child: DetailList(snapshot.data.details),
//                    )
//                  ],
//                ),
//              );
            }
            if (snapshot.connectionState == ConnectionState.none) {
              return Text('Push button');
            } else {
              return CircularProgressIndicator();
            }
          },
        )
      ],
    ))));
  }
}
