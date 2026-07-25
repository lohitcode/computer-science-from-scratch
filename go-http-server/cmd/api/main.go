package main

import (
	"fmt"

	"github.com/lohitcode/computer-science-from-scratch/go-http-server/internal/config"
	"github.com/lohitcode/computer-science-from-scratch/go-http-server/internal/httpserver"
)

func main() {

	cfg, configErr := config.Load()

	if configErr != nil {
		fmt.Println(configErr)
		return
	}

	router := httpserver.NewRouter()

	server := httpserver.NewServer(cfg.Port, router)
	fmt.Println("Server listening on http://localhost:", cfg.Port)
	serverError := server.ListenAndServe()

	if serverError != nil {
		fmt.Println(serverError)
	}

}
