package httpserver

import (
	"encoding/json"
	"net/http"
)

func healthHandler(w http.ResponseWriter, _ *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	response := map[string]string{
		"status": "ok",
	}

	json.NewEncoder(w).Encode(response)
}

func NewRouter() *http.ServeMux {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /health", healthHandler)

	return mux
}
