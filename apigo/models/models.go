package models

type Response struct {
	Name        string     `json:"name"`
	Description string     `json:"description"`
	Quality     float64    `json:"quality"`
	Location    *Location  `json:"location,omitempty"`
	Details     []Response `json:"details,omitempty"`
}

type Location struct {
	Lng float32 `json:"lng"`
	Lat float32 `json:"lat"`
}
