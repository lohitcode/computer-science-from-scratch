// =====================================================
// PROBLEM 19A: Context Values in HTTP Middleware
// =====================================================
// YOUR TASK: Use middleware to add a request ID to an
// HTTP request's context, then read it in a handler.
//
// 1. Define a private contextKey type.
// 2. Define requestIDKey using that type.
// 3. Create requestIDMiddleware(next http.Handler).
// 4. In the middleware, add "req-123" to r.Context()
//    with context.WithValue.
// 5. Attach the new context using r.WithContext(ctx).
// 6. Call the next handler with next.ServeHTTP(w, r).
// 7. In helloHandler, read and safely type-assert the
//    request ID, then write it to the response.
// 8. Wrap helloHandler with the middleware and serve it
//    at /hello on port 8080.
//
// Test it in another terminal with:
//   curl http://localhost:8080/hello
//
// Expected response:
//   Request ID: req-123
//
// Read lessons/context.md, especially Exercise 19A.
// Exercise 19B will cover cancellation and timeouts.
// =====================================================

package main

import (
	"context"
	"fmt"
	"net/http"
)

func generateRequestID() string {
	return "req-123"
}

type contextKey string

const requestIDKey contextKey = "requestID"

func helloHandler(w http.ResponseWriter, r *http.Request) {
	requestID, ok := r.Context().Value(requestIDKey).(string)

	if !ok {
		http.Error(w, "request ID missing", http.StatusInternalServerError)
		return
	}
	fmt.Fprintln(w, "Request ID:", requestID)
}

func requestIDMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ctx := context.WithValue(r.Context(), requestIDKey, generateRequestID())
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func main() {
	handler := http.HandlerFunc(helloHandler)
	wrapped := requestIDMiddleware(handler)
	http.Handle("/hello", wrapped)
	fmt.Println("Starting Server...")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("server error", err)
	}
}
