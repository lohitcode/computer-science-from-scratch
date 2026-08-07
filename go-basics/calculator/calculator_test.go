package calculator

import (
	"testing"
)

// TestAdd verifies that Add(2, 3) returns 5.
func TestAdd(t *testing.T) {
	got := Add(2, 3)
	want := 5
	if got != want {
		t.Errorf("the output should be 5 but got %d", got)
	}
}

// TestDivide verifies the normal case: Divide(10, 2) returns 5 and no error.
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

// TestDivideByZero verifies that Divide(10, 0) returns the expected error.
func TestDivideByZero(t *testing.T) {
	_, err := Divide(10, 0)
	if err == nil {
		t.Fatal("expected an error, got nil")
	}

	if err.Error() != "cannot divide by zero" {
		t.Errorf("error = %q; want %q", err.Error(), "cannot divide by zero")
	}

}
