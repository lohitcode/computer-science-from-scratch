#include <stdio.h>
#include <stdlib.h>

// =====================================================
// LESSON 33: CALLOC AND REALLOC
// =====================================================
// calloc(n, size)  - Allocate n items, zero-initialized
// realloc(ptr, size) - Resize existing allocation
//
// calloc vs malloc: calloc zeros memory, malloc has garbage
// realloc can grow or shrink, may move memory to new location
// =====================================================

void print_array(int *arr, int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

int main() {
    // Use calloc for array of 5 zeros
    int *arr = calloc(5, sizeof(int));

    if (arr == NULL) {
        printf("Allocation failed!\n");
        return 1;
    }

    printf("=== After calloc (5 zeros) ===\n");
    print_array(arr, 5);

    // Fill with values
    for (int i = 0; i < 5; i++) {
        arr[i] = (i + 1) * 10;
    }

    printf("=== After filling ===\n");
    print_array(arr, 5);

    // Use realloc to grow to 8 elements
    int *temp = realloc(arr, 8 * sizeof(int));
    if (temp == NULL) {
        printf("Realloc failed!\n");
        free(arr);
        return 1;
    }
    arr = temp;

    printf("=== After realloc grow to 8 ===\n");
    print_array(arr, 8);

    // Fill new elements
    for (int i = 5; i < 8; i++) {
        arr[i] = (i + 1) * 10;
    }

    printf("=== After filling new elements ===\n");
    print_array(arr, 8);

    // Use realloc to shrink to 3 elements
    temp = realloc(arr, 3 * sizeof(int));
    if (temp == NULL) {
        printf("Realloc failed!\n");
        free(arr);
        return 1;
    }
    arr = temp;

    printf("=== After realloc shrink to 3 ===\n");
    print_array(arr, 3);

    free(arr);
    printf("Memory freed!\n");

    return 0;
}
