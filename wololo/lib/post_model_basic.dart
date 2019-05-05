// To parse this JSON data, do
//
//     final post = postFromJson(jsonString);

import 'dart:convert';

Post postFromJson(String str) => Post.fromJson(json.decode(str));

String postToJson(Post data) => json.encode(data.toJson());

class Post {
  String name;
  String description;
  double quality;
  Location location;
  List<Detail> details;

  Post({
    this.name,
    this.description,
    this.quality,
    this.location,
    this.details,
  });

  factory Post.fromJson(Map<String, dynamic> json) => new Post(
    name: json["name"],
    description: json["description"],
    quality: json["quality"].toDouble(),
    location: Location.fromJson(json["location"]),
    details: new List<Detail>.from(json["details"].map((x) => Detail.fromJson(x))),
  );

  Map<String, dynamic> toJson() => {
    "name": name,
    "description": description,
    "quality": quality,
    "location": location.toJson(),
    "details": new List<dynamic>.from(details.map((x) => x.toJson())),
  };
}

class Detail {
  String name;
  String description;
  double quality;

  Detail({
    this.name,
    this.description,
    this.quality,
  });

  factory Detail.fromJson(Map<String, dynamic> json) => new Detail(
    name: json["name"],
    description: json["description"],
    quality: json["quality"].toDouble(),
  );

  Map<String, dynamic> toJson() => {
    "name": name,
    "description": description,
    "quality": quality,
  };
}

class Location {
  double lng;
  double lat;

  Location({
    this.lng,
    this.lat,
  });

  factory Location.fromJson(Map<String, dynamic> json) => new Location(
    lng: json["lng"].toDouble(),
    lat: json["lat"].toDouble(),
  );

  Map<String, dynamic> toJson() => {
    "lng": lng,
    "lat": lat,
  };
}
