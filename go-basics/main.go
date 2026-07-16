// =====================================================
// PROBLEM 16: Files and I/O
// =====================================================
// YOUR TASK: Write text to a file, then read it back.
//
// 1. Store "Learning Go files!" in a byte slice.
// 2. Write it to notes.txt with os.WriteFile.
// 3. Handle the write error.
// 4. Read notes.txt with os.ReadFile.
// 5. Handle the read error.
// 6. Convert the returned bytes to a string and print it.
//
// Expected output:
//   Learning Go files!
//
// Read lessons/files-and-io.md before starting.
// =====================================================

package main

import (
	"fmt"
	"os"
)

func main() {
	text := "Learning Go files!"
	bytes := []byte(text)
	filename := "notes.txt"
	err := os.WriteFile(filename, bytes, 0644)

	if err != nil {
		fmt.Printf("File write error: %s", err)
		return
	}

	data, err := os.ReadFile(filename)

	if err != nil {
		fmt.Printf("File read error: %s", err)
		return
	}

	fmt.Println(string(data))
}
