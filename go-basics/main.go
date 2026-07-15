// =====================================================
// PROBLEM 13: Packages & Modules
// =====================================================
// YOUR TASK: Create and use your own calculator package.
//
// Expected output:
//   Packages & Modules!
//   5 + 3 = 8
//   5 - 3 = 2
//   5 * 3 = 15
//
// Read lessons/packages-and-modules.md before starting.
// =====================================================

package main

import (
	"fmt"
	"go-basics/calculator"
)

// TODO 1: Initialize this project as a Go module:
//   go mod init go-basics
//
// TODO 2: Create calculator/calculator.go.
//
// TODO 3: Export Add, Subtract, and Multiply from package calculator.
//
// TODO 4: Import your package:
//   "go-basics/calculator"
//
// TODO 5: Call the three calculator functions from main.

func main() {
	fmt.Println("Packages & Modules!")

	fmt.Printf("1 + 2 = %d\n", calculator.Add(1, 2))
	fmt.Printf("2 - 1 = %d\n", calculator.Subtract(2, 1))
	fmt.Printf("2 * 2 = %d\n", calculator.Multiply(2, 2))
}
