// =====================================================
// DSA PROBLEM 1: Big O and Linear Search
// =====================================================
// YOUR TASK: Find a target value by scanning a slice.
//
// Implement:
//   func linearSearch(numbers []int, target int) int
//
// Rules:
// 1. Check the numbers from left to right.
// 2. Return the index of the first matching value.
// 3. Return -1 when the target is not present.
// 4. Do not use a map or a sorting function.
//
// Read lessons/big-o-and-linear-search.md first.
// Write code only inside the marked solution area.
// =====================================================

package main

import (
	"fmt"
	"os"
)

// ==================== SOLUTION AREA ====================

func linearSearch(numbers []int, target int) int {
	// TODO: Write your solution here.
	return -2
}

// ================== END SOLUTION AREA ==================

type testCase struct {
	name     string
	numbers  []int
	target   int
	expected int
}

func main() {
	tests := []testCase{
		{
			name:     "target in the middle",
			numbers:  []int{4, 2, 9, 7, 5},
			target:   7,
			expected: 3,
		},
		{
			name:     "target is missing",
			numbers:  []int{4, 2, 9, 7, 5},
			target:   10,
			expected: -1,
		},
		{
			name:     "first duplicate is returned",
			numbers:  []int{7, 2, 7},
			target:   7,
			expected: 0,
		},
		{
			name:     "empty slice",
			numbers:  []int{},
			target:   7,
			expected: -1,
		},
		{
			name:     "single matching element",
			numbers:  []int{7},
			target:   7,
			expected: 0,
		},
		{
			name:     "single non-matching element",
			numbers:  []int{4},
			target:   7,
			expected: -1,
		},
		{
			name:     "negative target",
			numbers:  []int{0, -2, 5},
			target:   -2,
			expected: 1,
		},
	}

	passed := 0

	for number, test := range tests {
		actual := linearSearch(test.numbers, test.target)

		if actual != test.expected {
			fmt.Printf(
				"FAIL %d: %s — expected %d, got %d\n",
				number+1,
				test.name,
				test.expected,
				actual,
			)
			continue
		}

		fmt.Printf("PASS %d: %s\n", number+1, test.name)
		passed++
	}

	fmt.Printf("\n%d/%d tests passed\n", passed, len(tests))

	if passed != len(tests) {
		os.Exit(1)
	}
}
