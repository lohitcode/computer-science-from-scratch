package calculator

import (
	"testing"
)

// TODO 1: Write TestAdd.
// Call Add(2, 3) and fail the test if the result is not 5.
func TestAdd(t *testing.T) {
	got := Add(2, 3)
	want := 5
	if got != want {
		t.Errorf("the output should be 5 but got %d", got)
	}
}

// TODO 2: Write TestDivide.
// Call Divide(10, 2) and check both returned values:
// the result must be 5 and the error must be nil.
func TestDivide(t *testing.T) {
	got, err := Divide(10, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	want := 5
	if got != want {
		t.Errorf("the output should be 5 but got %s", err)
	}
}

// TODO 3: Write TestDivideByZero.
// Call Divide(10, 0) and verify that:
//   - an error is returned
//   - err.Error() equals "cannot divide by zero"

func TestDivideByZero(t *testing.T) {
	_, err := Divide(10, 0)
	if err == nil {
		t.Fatal("expected an error, got nil")
	}

	if err.Error() != "cannot divide by zero" {
		t.Errorf("error = %q; want %q", err.Error(), "cannot divide by zero")
	}

}

// This reference keeps the testing import valid until you write the tests.
