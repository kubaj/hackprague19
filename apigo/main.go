package main

import (
	"hackprague/airquality"
	"hackprague/apipython"
	"net/http"
	"os"

	"github.com/labstack/echo"
)

type Response struct {
	Name        string     `json:"name"`
	Description string     `json:"description"`
	Quality     float64    `json:"quality"`
	Details     []Response `json:"details"`
}

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

		qualities := []Response{}
		sum := 0.0

		air, err := airquality.FetchAirquality(geo.Latitude, geo.Longitude)
		if err == nil {
			sum += air
			qualities = append(qualities, Response{Name: "Air quality", Quality: air, Description: "", Details: []Response{}})
		}

		return c.JSON(http.StatusOK, Response{Name: "Overall", Description: "Overall quality of life on this address", Quality: sum / float64(len(qualities)), Details: qualities})
	})
	e.Logger.Fatal(e.Start(":" + serverPort))
}
