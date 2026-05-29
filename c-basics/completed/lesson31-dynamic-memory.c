#include <stdio.h>
#include <stdlib.h>

// =====================================================
// LESSON 31: WHAT IS DYNAMIC MEMORY?
// =====================================================
// Stack: Automatic, limited size, destroyed when function returns
// Heap: Manual, large size, survives until you free it
//
// Why dynamic memory?
// 1. Size unknown at compile time
// 2. Data must survive beyond function scope
//
// Pattern: malloc → check NULL → use → free → set NULL
// =====================================================

int main() {
    // Allocate memory for one integer on heap
    int *ptr = malloc(sizeof(int));

    // ALWAYS check if allocation succeeded
    if (ptr == NULL) {
        printf("Malloc failed!\n");
        return 1;
    }

    // Use the memory
    *ptr = 42;
    printf("Value: %d\n", *ptr);

    // Free the memory when done
    free(ptr);
    ptr = NULL;  // Good practice: prevent use-after-free

    printf("Memory freed successfully!\n");

    return 0;
}
