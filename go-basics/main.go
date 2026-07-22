// =====================================================
// PROBLEM 18: HTTP Servers and Handlers
// =====================================================
// YOUR TASK: Build a small HTTP server using net/http.
//
// 1. Create a helloHandler function with the standard
//    http.HandlerFunc signature.
// 2. Write "Hello from Go!" to the response.
// 3. Register the handler at the /hello path.
// 4. Print "Server listening on http://localhost:8080".
// 5. Start the server on port 8080.
// 6. Handle the error returned by ListenAndServe.
//
// Test it in another terminal with:
//   curl http://localhost:8080/hello
//
// Expected curl output:
//   Hello from Go!
//
// Read lessons/http-servers.md before starting.
// =====================================================

package main

import (
	"fmt"
	"net/http"
	"os"
)

func helloHandler(w http.ResponseWriter, _ *http.Request) {
	fmt.Print()
	fmt.Fprint(w, "Hello from Go!")
}

func main() {
	http.HandleFunc("/hello", helloHandler)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8000"
	}
	fmt.Println("Server Started on port ", port)

	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		fmt.Println("server error: ", err)
		return
	}
}
