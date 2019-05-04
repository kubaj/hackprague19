package apipython

import (
	"encoding/json"
	"errors"
	"fmt"
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
