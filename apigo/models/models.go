package models

type Response struct {
	Name        string     `json:"name"`
	Description string     `json:"description"`
	Quality     float64    `json:"quality"`
	Details     []Response `json:"details"`
}
