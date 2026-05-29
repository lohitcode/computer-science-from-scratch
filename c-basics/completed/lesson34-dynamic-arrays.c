#include <stdio.h>
#include <stdlib.h>

// =====================================================
// LESSON 34: DYNAMIC ARRAYS
// =====================================================
// Arrays that grow as needed using realloc
//
// Pattern:
//   1. Start with initial capacity
//   2. Track size and capacity
//   3. When size == capacity, realloc to grow
//   4. Common strategy: double the capacity
// =====================================================

// Dynamic array structure
typedef struct {
    int *data;      // The array
    int size;       // Current elements
    int capacity;   // Total space
} DynamicArray;

// Initialize dynamic array
void init_array(DynamicArray *arr, int initial_capacity) {
    arr->data = malloc(initial_capacity * sizeof(int));
    arr->size = 0;
    arr->capacity = initial_capacity;
}

// Append element (grow if needed)
void append(DynamicArray *arr, int value) {
    // Check if needs to grow
    if (arr->size == arr->capacity) {
        arr->capacity = arr->capacity * 2;  // Double strategy
        printf("Growing capacity to %d\n", arr->capacity);
        int *temp = realloc(arr->data, arr->capacity * sizeof(int));
        if (temp == NULL) {
            printf("Realloc failed!\n");
            return;
        }
        arr->data = temp;
    }

    // Add value
    arr->data[arr->size++] = value;
}

// Print array status
void print_status(DynamicArray *arr) {
    printf("Size: %d, Capacity: %d\n", arr->size, arr->capacity);
    printf("Elements: ");
    for (int i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("\n\n");
}

// Cleanup
void cleanup(DynamicArray *arr) {
    free(arr->data);
    arr->data = NULL;
    arr->size = 0;
    arr->capacity = 0;
}

int main() {
    DynamicArray arr;
    init_array(&arr, 5);  // Start with capacity 5

    printf("=== Initial State ===\n");
    print_status(&arr);

    // Add elements and watch it grow!
    for (int i = 1; i <= 15; i++) {
        append(&arr, i * 10);

        if (i % 5 == 0) {
            printf("=== After adding %d elements ===\n", i);
            print_status(&arr);
        }
    }

    cleanup(&arr);
    printf("Memory freed!\n");

    return 0;
}
