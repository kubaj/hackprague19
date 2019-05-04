package airquality

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
)

type Response struct {
	Results []Result `json="results"`
}

type Result struct {
	Measurements []Measurement `json="measurements"`
}

type Measurement struct {
	Parameter string  `json="parameter"`
	Value     float64 `json="value"`
}

func FetchAirquality(lat float32, lng float32) (float64, error) {
	resp, err := http.Get(fmt.Sprintf("https://api.openaq.org/v1/latest?coordinates=%.9f,%.9f", lat, lng))
	if err != nil {
		return 0, err
	}

	if resp.StatusCode != http.StatusOK {
		return 0, errors.New("Failed to fetch air quality")
	}

	locationResponse := &Response{}
	err = json.NewDecoder(resp.Body).Decode(locationResponse)
	if err != nil {
		return 0, err
	}

	if len(locationResponse.Results) == 0 {
		return 0, errors.New("No datapoints for location")
	}

	count := 0
	sum := 0.0

	for _, measurement := range locationResponse.Results[0].Measurements {
		if measurement.Parameter == "no2" {
			sum += 1.0 - measurement.Value/200
		} else if measurement.Parameter == "co" {
			sum += 1.0 - measurement.Value/5000
		} else if measurement.Parameter == "pm10" {
			sum += 1.0 - measurement.Value/400
		} else if measurement.Parameter == "pm25" {
			sum += 1.0 - measurement.Value/200
		} else {
			count--
		}
		count++
	}

	return 10 * sum / float64(count), nil
}
