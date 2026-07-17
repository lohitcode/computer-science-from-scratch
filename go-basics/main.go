// =====================================================
// PROBLEM 17: JSON Encoding and Decoding
// =====================================================
// YOUR TASK: Convert a Go struct to JSON, then convert
// that JSON back into a Go struct.
//
// 1. Create a Progress struct with Name and Completed.
// 2. Give both fields JSON tags using lowercase names.
// 3. Create: Progress{Name: "Lohit", Completed: 16}
// 4. Encode it with json.Marshal and handle the error.
// 5. Print the JSON string.
// 6. Decode it into a new Progress value with
//    json.Unmarshal and handle the error.
// 7. Print the decoded fields.
//
// Expected output:
//   JSON: {"name":"Lohit","completed":16}
//   Decoded: Lohit completed 16 lessons
//
// Read lessons/json.md before starting.
// =====================================================

package main

import (
	"encoding/json"
	"fmt"
)

type Progress struct {
	Name      string `json:"name"`
	Completed int    `json:"completed"`
}

func main() {
	lohit := Progress{Name: "Lohit", Completed: 16}

	data, err := json.Marshal(lohit)

	if err != nil {
		fmt.Println("Marshal error:", err)
		return
	}

	fmt.Printf("JSON: %s\n", string(data))

	var unmarshaled Progress
	unmarshalErr := json.Unmarshal(data, &unmarshaled)

	if unmarshalErr != nil {
		fmt.Println("Unmarshal error:", unmarshalErr)
		return
	}

	fmt.Printf(
		"Decoded: %s completed %d lessons\n",
		unmarshaled.Name,
		unmarshaled.Completed,
	)
}
