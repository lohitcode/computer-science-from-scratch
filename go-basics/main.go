// =====================================================
// PROBLEM 19B: Context Timeout and Cancellation
// =====================================================
// YOUR TASK: Stop slow work when its context expires.
//
// 1. Create slowOperation(ctx context.Context) error.
// 2. Inside it, select between:
//      time.After(2 * time.Second)
//      ctx.Done()
// 3. Return nil if the work finishes first.
// 4. Return ctx.Err() if cancellation happens first.
// 5. In main, create a context with a 500 ms timeout.
// 6. Defer its cancel function.
// 7. Call slowOperation and print its returned error.
//
// Expected output after about 500 ms:
//   Starting slow operation...
//   Operation stopped: context deadline exceeded
//
// Read Exercise 19B in lessons/context.md.
// =====================================================

package main

import (
	"context"
	"fmt"
	"time"
)

func slowOperation(ctx context.Context) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-time.After(2 * time.Second):
		return nil
	}
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()
	fmt.Println("Starting slow operation...")
	err := slowOperation(ctx)
	if err != nil {
		fmt.Println("Operation stopped:", err)
	}
}
