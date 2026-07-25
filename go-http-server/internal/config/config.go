package config

import (
	"errors"
	"os"
	"strconv"
)

type Config struct {
	Port string
}

var (
	ErrMissing = errors.New("config error: PORT Missing")
	ErrInvalid = errors.New("config error: PORT must be a base-10 int")
	ErrBound   = errors.New("config error: PORT out of bound")
)

func Load() (Config, error) {

	portString, exists := os.LookupEnv("PORT")

	if !exists || portString == "" {
		return Config{}, ErrMissing
	}

	port, err := strconv.Atoi(portString)

	if err != nil {
		return Config{}, ErrInvalid
	}

	if port < 1 || port > 65535 {
		return Config{}, ErrBound
	}

	return Config{Port: strconv.Itoa(port)}, nil
}
