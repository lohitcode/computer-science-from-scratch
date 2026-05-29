#include <stdio.h>

// =====================================================
// LESSON 20: POINTERS AND FUNCTIONS
// =====================================================
// Problem: Parameters are copies - can't modify originals
// Solution: Pass pointers to modify original variables
//
// Pattern:
//   Definition: void func(int *ptr)
//   Call:      func(&variable)
// =====================================================

// Function that triples a value
void triple(int *ptr) {
    *ptr = *ptr * 3;
}

// Function that swaps two values
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Function that sets to zero
void set_to_zero(int *ptr) {
    *ptr = 0;
}

// Function that adds 10
void add_ten(int *ptr) {
    *ptr = *ptr + 10;
}

// Function that squares a value
void square(int *ptr) {
    *ptr = *ptr * *ptr;
}

int main() {
    // Test triple
    printf("=== Triple ===\n");
    int num = 5;
    printf("Before triple: %d\n", num);
    triple(&num);
    printf("After triple: %d\n\n", num);

    // Test swap
    printf("=== Swap ===\n");
    int x = 10, y = 20;
    printf("Before swap: x=%d, y=%d\n", x, y);
    swap(&x, &y);
    printf("After swap: x=%d, y=%d\n\n", x, y);

    // Test set_to_zero
    printf("=== Set to Zero ===\n");
    int value = 100;
    printf("Before: %d\n", value);
    set_to_zero(&value);
    printf("After: %d\n\n", value);

    // Test add_ten
    printf("=== Add Ten ===\n");
    int age = 25;
    printf("Before: %d\n", age);
    add_ten(&age);
    printf("After: %d\n\n", age);

    // Test square
    printf("=== Square ===\n");
    int base = 4;
    printf("Before: %d\n", base);
    square(&base);
    printf("After: %d\n", base);

    return 0;
}
