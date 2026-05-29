#include <stdio.h>

// =====================================================
// LESSON 21: POINTERS AND ARRAYS
// =====================================================
// Big Secret: Array names "decay" to pointers!
// arr[i] is actually *(arr + i) in disguise.
//
// Pattern:
//   *arr        = first element (arr[0])
//   *(arr + 1)  = second element (arr[1])
//   *(arr + n)  = element at index n (arr[n])
// =====================================================

// Return first element using pointer dereference
int get_first(int *arr, int size) {
    (void)size;  // Unused parameter (first element doesn't need size)
    return *arr;
}

// Return last element using pointer arithmetic
int get_last(int *arr, int size) {
    return *(arr + size - 1);
}

// Sum all elements using pointer notation (not array indexing)
int sum_array(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum = sum + *(arr + i);
    }
    return sum;
}

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int size = 5;

    // Test get_first
    printf("=== Get First ===\n");
    printf("First element: %d\n\n", get_first(numbers, size));

    // Test get_last
    printf("=== Get Last ===\n");
    printf("Last element: %d\n\n", get_last(numbers, size));

    // Test sum_array
    printf("=== Sum Array ===\n");
    printf("Sum of all elements: %d\n", sum_array(numbers, size));

    return 0;
}
