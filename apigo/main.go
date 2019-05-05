package main

import (
	"context"
	"fmt"
	"hackprague/airquality"
	"hackprague/apipython"
	"hackprague/models"
	"log"
	"net/http"
	"os"

	"cloud.google.com/go/bigquery"
	"github.com/labstack/echo"
)

type BQProcessor struct {
	U *bigquery.Uploader
}

func main() {
	serverPort := os.Getenv("PORT")
	if serverPort == "" {
		serverPort = "8080"
	}

	ctx := context.Background()
	client, err := bigquery.NewClient(ctx, "hackprague19")
	if err != nil {
		log.Fatalf("error initializing bigquery: %v", err)
	}

	u := client.Dataset("heatmap").Table("data").Uploader()
	bqp := BQProcessor{
		U: u,
	}

	bqStream := make(chan models.Response)

	go bqp.ProcessBigquery(bqStream)

	e := echo.New()
	e.GET("/", func(c echo.Context) error {

		address := c.QueryParam("address")
		if address == "" {
			return c.JSON(http.StatusBadRequest, nil)
		}

		geo, err := apipython.GetCoordinates(address)
		if err != nil {
			return c.JSON(http.StatusBadGateway, nil)
		}

		qualities := []models.Response{}
		sum := 0.0
		count := 0

		air, err := airquality.FetchAirquality(geo.Latitude, geo.Longitude)
		if err == nil {
			sum += air
			count++
			qualities = append(qualities, models.Response{Name: "Air quality", Quality: air, Description: "Air quality in surrounding areas. Takes into considerations levels of CO2, SO2, particles of size PM10 and PM2.5", Details: []models.Response{}})
		}

		additional, err := apipython.GetAdditionalQualities(geo.Latitude, geo.Longitude)
		if err != nil {
			return c.JSON(http.StatusBadGateway, nil)
		}

		for _, quality := range additional.Details {
			qualities = append(qualities, quality)
			sum += quality.Quality
		}
		count += len(additional.Details)

		response := models.Response{
			Name:        "Overall",
			Description: "Overall quality of life on this address",
			Quality:     sum / float64(count),
			Details:     qualities,
			Location: &models.Location{
				Lng: geo.Longitude,
				Lat: geo.Latitude,
			},
		}

		bqStream <- response

		return c.JSON(http.StatusOK, response)
	})
	e.Logger.Fatal(e.Start(":" + serverPort))
}

type BQModel struct {
	Coordinates string
	Name        string
	Value       float64
}

func (b *BQProcessor) ProcessBigquery(stream chan models.Response) {
	for {
		select {
		case item := <-stream:
			coord := fmt.Sprintf("%.9f,%.9f", item.Location.Lat, item.Location.Lng)
			items := []*BQModel{
				{Name: item.Name, Value: item.Quality, Coordinates: coord},
			}
			for _, detail := range item.Details {
				items = append(items, &BQModel{Name: detail.Name, Value: detail.Quality, Coordinates: coord})
			}

			err := b.U.Put(context.Background(), items)
			if err != nil {
				log.Printf("Failed to push data to bigquery: %v", err)
			}
		}
	}
}
