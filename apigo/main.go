package main

import (
	"hackprague/airquality"
	"hackprague/apipython"
	"hackprague/models"
	"net/http"
	"os"

	"github.com/labstack/echo"
)

func main() {
	serverPort := os.Getenv("PORT")
	if serverPort == "" {
		serverPort = "8080"
	}

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

		return c.JSON(http.StatusOK, models.Response{Name: "Overall", Description: "Overall quality of life on this address", Quality: sum / float64(count), Details: qualities})
	})
	e.Logger.Fatal(e.Start(":" + serverPort))
}
