#include <stdio.h>
#include <stdlib.h>

// =====================================================
// LESSON 25: DOUBLE POINTERS
// =====================================================
// A pointer to another pointer: int **
//
// Why? To modify a pointer INSIDE a function
// Same logic as why we use pointers to modify variables
//
// *dptr  - gets the pointer
// **dptr - gets the value
// =====================================================

// Allocate memory for int and set value
void allocate_int(int **ptr, int value) {
    *ptr = malloc(sizeof(int));  // Modify the pointer itself
    **ptr = value;               // Set the value
}

// Set pointer to NULL
void nullify(int **ptr) {
    *ptr = NULL;
}

// Make ptr point to a different target
void modify_pointer(int **ptr, int *new_target) {
    *ptr = new_target;
}

int main() {
    // Test allocate_int
    printf("=== Allocate Int ===\n");
    int *ptr = NULL;
    allocate_int(&ptr, 42);
    printf("Value: %d\n\n", *ptr);
    free(ptr);

    // Test nullify
    printf("=== Nullify ===\n");
    int x = 100;
    ptr = &x;
    printf("Before nullify: %p\n", (void*)ptr);
    nullify(&ptr);
    printf("After nullify: %p\n\n", (void*)ptr);

    // Test modify_pointer
    printf("=== Modify Pointer ===\n");
    int a = 10, b = 20;
    ptr = &a;
    printf("Points to: %d\n", *ptr);
    modify_pointer(&ptr, &b);
    printf("Now points to: %d\n", *ptr);

    return 0;
}
