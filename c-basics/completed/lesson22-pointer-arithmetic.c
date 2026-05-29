#include <stdio.h>

// =====================================================
// LESSON 22: POINTER ARITHMETIC
// =====================================================
// Adding to pointers moves by sizeof(type), not 1 byte
// ptr + 1 on int* moves 4 bytes (to next int)
//
// Operations:
//   ptr++   - move to next element
//   ptr--   - move to previous element
//   ptr + n - move n elements ahead
//   p2 - p1 - distance in elements (not bytes!)
// =====================================================

// Return pointer to the largest element
int *find_max(int *arr, int size) {
    int *max_ptr = arr;      // Start: first element is max
    int *end = arr + size;   // Pointer to "one past end"

    while (arr < end) {
        if (*arr > *max_ptr) {
            max_ptr = arr;    // Update max pointer
        }
        arr++;               // Move to next element
    }

    return max_ptr;
}

// Count how many times target appears
int count_occurrences(int *arr, int size, int target) {
    int count = 0;
    int *end = arr + size;

    while (arr < end) {
        if (*arr == target) {
            count++;
        }
        arr++;
    }

    return count;
}

// Find target, return pointer (or NULL if not found)
int *find_value(int *arr, int size, int target) {
    int *end = arr + size;

    while (arr < end) {
        if (*arr == target) {
            return arr;      // Found it - return pointer
        }
        arr++;
    }

    return NULL;             // Not found
}

int main() {
    int numbers[8] = {5, 3, 9, 1, 9, 7, 2, 9};
    int size = 8;

    // Test find_max
    printf("=== Find Max ===\n");
    int *max = find_max(numbers, size);
    printf("Max value: %d\n\n", *max);

    // Test count_occurrences
    printf("=== Count Occurrences ===\n");
    printf("Count of 9: %d\n", count_occurrences(numbers, size, 9));
    printf("Count of 5: %d\n\n", count_occurrences(numbers, size, 5));

    // Test find_value
    printf("=== Find Value ===\n");
    int *found = find_value(numbers, size, 7);
    if (found != NULL) {
        printf("Found 7 at position: %ld\n", found - numbers);
    }

    found = find_value(numbers, size, 99);
    if (found == NULL) {
        printf("99 not found\n");
    }

    return 0;
}
