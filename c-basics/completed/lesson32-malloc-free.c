#include <stdio.h>
#include <stdlib.h>

// =====================================================
// LESSON 32: MALLOC AND FREE
// =====================================================
// malloc(size)  - Allocate memory on heap
// free(ptr)     - Release memory back to system
//
// Pattern:
//   1. malloc
//   2. Check NULL
//   3. Use memory
//   4. free
//   5. Set to NULL
// =====================================================

int main() {
    int n = 5;

    // Allocate array of n integers
    int *arr = malloc(n * sizeof(int));

    // ALWAYS check if allocation succeeded
    if (arr == NULL) {
        printf("Malloc failed!\n");
        return 1;
    }

    // Fill array with values
    for (int i = 0; i < n; i++) {
        arr[i] = (i + 1) * 10;
    }

    // Print the array
    printf("Array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");

    // Free the memory
    free(arr);
    arr = NULL;

    printf("Memory freed!\n");

    return 0;
}
