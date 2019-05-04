package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo"
)

type Request struct {
	Address string `json:"address"`
}

type Response struct {
	Name        string     `json:"name"`
	Description string     `json:"description"`
	Quality     float32    `json:"quality"`
	Details     []Response `json:"details"`
}

func main() {
	serverPort := os.Getenv("PORT")
	if serverPort == "" {
		serverPort = "8080"
	}

	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		req := new(Request)
		if err := c.Bind(req); err != nil {
			return err
		}

		return c.JSON(http.StatusOK, Response{Name: "Overall", Description: "Overall quality of life on this address", Quality: 8.9, Details: []Response{}})
	})
	e.Logger.Fatal(e.Start(":" + serverPort))
}
