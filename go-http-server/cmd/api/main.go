package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func main() {
	fmt.Println("Starting Server...")
	mux := http.NewServeMux()

	mux.HandleFunc("GET /health", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")

		response := map[string]string{
			"status": "ok",
		}

		json.NewEncoder(w).Encode(response)
	})

	server := &http.Server{
		Addr:              ":8080",
		Handler:           mux,
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       60 * time.Second,
	}

	err := server.ListenAndServe()

	if err != nil {
		fmt.Println("Server Error: ", err)
	}

}
