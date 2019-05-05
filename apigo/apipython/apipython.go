package apipython

import (
	"encoding/json"
	"errors"
	"fmt"
	"hackprague/models"
	"net/http"
	"net/url"
)

const apiPythonAddress = "https://apipython-6um4xsxxgq-uc.a.run.app"

type Response struct {
	Latitude  float32 `json="latitude"`
	Longitude float32 `json="longitude"`
}

func GetCoordinates(address string) (*Response, error) {
	url := fmt.Sprintf("%s/geocode?address=%s", apiPythonAddress, url.QueryEscape(address))
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		return nil, errors.New("Failed to fetch geodata")
	}

	response := &Response{}
	err = json.NewDecoder(resp.Body).Decode(response)
	return response, err
}

func GetAdditionalQualities(lat float32, lng float32) (*models.Response, error) {
	url := fmt.Sprintf("%s/places?lat=%.9f&lng=%.9f", apiPythonAddress, lat, lng)

	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		return nil, errors.New("Failed to fetch additional qualities")
	}

	response := &models.Response{}
	err = json.NewDecoder(resp.Body).Decode(response)
	if err != nil {
		return nil, err
	}

	for i := range response.Details {
		response.Details[i].Quality = response.Details[i].Quality * float64(10)
	}

	return response, nil
}
