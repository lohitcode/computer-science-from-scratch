#include <stdio.h>

// =====================================================
// LESSON 24: CONST AND POINTERS
// =====================================================
// const means "cannot modify" - read-only
//
// Three types:
//   const int *ptr        - Can't change VALUE (data is const)
//   int *const ptr        - Can't change POINTER (pointer is const)
//   const int *const ptr  - Can't change EITHER
//
// Read right-to-left to understand:
//   const int *ptr  -> "ptr is pointer to const int"
// =====================================================

// Sum array - const because we only READ, not modify
int sum_array(const int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];  // Reading is OK
    }
    return sum;
}

// Fill array with value - NO const because we WILL modify
void fill_with(int *arr, int size, int value) {
    for (int i = 0; i < size; i++) {
        arr[i] = value;  // Modifying is OK (no const)
    }
}

// Find max - const because we only READ
int find_max(const int *arr, int size) {
    int max = arr[0];
    for (int i = 1; i < size; i++) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    return max;
}

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    int size = 5;

    // Test sum_array (doesn't modify - const parameter)
    printf("=== Sum Array (const, read-only) ===\n");
    printf("Sum: %d\n", sum_array(numbers, size));
    printf("After sum: ");
    for (int i = 0; i < size; i++) printf("%d ", numbers[i]);
    printf("\n\n");

    // Test fill_with (modifies - no const)
    printf("=== Fill With (non-const, modifies) ===\n");
    fill_with(numbers, size, 99);
    printf("After fill: ");
    for (int i = 0; i < size; i++) printf("%d ", numbers[i]);
    printf("\n\n");

    // Test find_max (doesn't modify - const parameter)
    printf("=== Find Max (const, read-only) ===\n");
    printf("Max: %d\n", find_max(numbers, size));

    return 0;
}
