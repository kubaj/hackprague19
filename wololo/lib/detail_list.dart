import 'package:flutter/material.dart';
import 'package:percent_indicator/linear_percent_indicator.dart';
import 'package:wololo/post_model_basic.dart';

class WololoWidget extends StatelessWidget {
  WololoWidget(this.item);

  Detail item;

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: EdgeInsets.all(10),
        child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: <Widget>[
                  Text(
                    item.name,
                    style: TextStyle(
                      fontSize: 18,
                    ),
                  ),
                  LinearPercentIndicator(
                    width: 200,
                    lineHeight: 20,
                    percent: item.quality == 0 ? 0.05 : item.quality / 10,
                    progressColor: setProgressColor(item.quality),
                    animationDuration: 250,
                    animation: true,
                  ),
                ],
              ),
              Text(
                item.description,
              ),
            ]));
  }

  Color setProgressColor(double quality) {
    if (quality < 2) {
      return Color.fromRGBO(183, 36, 43, 1);
    } else if (quality >= 2 && quality < 4) {
      return Color.fromRGBO(181, 86, 29, 1);
    } else if (quality >= 4 && quality < 6) {
      return Color.fromRGBO(179, 148, 23, 1);
    } else if (quality >= 6 && quality < 8) {
      return Color.fromRGBO(142, 177, 17, 1);
    } else {
      return Color.fromRGBO(69, 176, 12, 1);
    }
  }
}
