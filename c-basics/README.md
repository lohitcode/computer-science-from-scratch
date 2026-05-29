# Chapter 10, Lesson 34: Dynamic Arrays

## What is a Dynamic Array?

An array that **grows as needed**! Unlike fixed arrays, you can add elements beyond the initial size.

---

## Fixed Array vs Dynamic Array

### Fixed Array (Lesson 13)

```c
int arr[100];  // Fixed size, can't grow!
```

### Dynamic Array (This Lesson)

```c
int *arr = malloc(10 * sizeof(int));  // Start with 10
arr = realloc(arr, 20 * sizeof(int));  // Grow to 20!
arr = realloc(arr, 50 * sizeof(int));  // Grow to 50!
```

---

## Why Dynamic Arrays?

```c
// Problem: Don't know how many items beforehand
int main() {
    int n;
    printf("How many numbers? ");
    scanf("%d", &n);  // User enters 1000

    int *arr = malloc(n * sizeof(int));  // Allocate exactly what we need!
    // Process n numbers...
}
```

---

## Pattern: Append to Dynamic Array

```c
int *arr = malloc(5 * sizeof(int));  // Start with capacity 5
int size = 0;        // Current elements
int capacity = 5;    // Total space

// Add elements:
while (need_to_add) {
    if (size == capacity) {
        // Grow! Double the capacity
        capacity = capacity * 2;
        arr = realloc(arr, capacity * sizeof(int));
    }
    arr[size++] = next_value;  // Add element
}
```

---

## Visual: Growing Array

```
Start:
Capacity: 5
Size: 0
[ ?][ ?][ ?][ ?][ ?]
 0  1  2  3  4

Add 3 elements:
Size: 3, Capacity: 5
[10][20][30][ ?][ ?]
 0   1   2   3   4

Try to add 4th (size would be 5, but capacity is 5):
Need to grow!

After realloc (double capacity):
Capacity: 10, Size: 5
[10][20][30][40][ ?][ ?][ ?][ ?][ ?][ ?]
 0   1   2   3   4   5   6   7   8   9
                    ↑
                Can add up to 10 now!
```

---

## Complete Example

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int capacity = 5;       // Start with 5
    int size = 0;           // No elements yet
    int *arr = malloc(capacity * sizeof(int));

    // Add elements dynamically
    for (int i = 0; i < 15; i++) {  // Adding 15 elements
        // Check if need to grow
        if (size == capacity) {
            capacity = capacity * 2;  // Double!
            printf("Growing to %d\n", capacity);
            arr = realloc(arr, capacity * sizeof(int));
        }

        arr[size++] = (i + 1) * 10;  // Add element
    }

    printf("Final array (%d elements):\n", size);
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }

    free(arr);
    return 0;
}
```

---

## Growth Strategies

### Strategy 1: Double (Common)

```c
if (size == capacity) {
    capacity = capacity * 2;  // 5 → 10 → 20 → 40...
}
```

**Pros:** Fast amortized (fewer reallocs)
**Cons:** Might waste memory

### Strategy 2: Fixed Increment

```c
if (size == capacity) {
    capacity = capacity + 10;  // Always add 10
}
```

**Pros:** Predictable
**Cons:** More reallocs = slower

### Strategy 3: Multiply by Factor

```c
if (size == capacity) {
    capacity = capacity * 1.5;  // Grow by 50%
}
```

**Middle ground** - common in real implementations!

---

## Your Task

Create a dynamic array that:

1. Starts with capacity 5
2. Doubles when full
3. Tracks size and capacity
4. Can append elements
5. Prints array status

---

## Starter Code (main.c)

```c
#include <stdio.h>
#include <stdlib.h>

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
    // TODO: Check if needs to grow
    if (arr->size == arr->capacity) {
        arr->capacity = arr->capacity * 2;
        printf("Growing capacity to %d\n", arr->capacity);
        arr->data = realloc(arr->data, arr->capacity * sizeof(int));
    }

    // TODO: Add value
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
```

---

## Expected Output

```
=== Initial State ===
Size: 0, Capacity: 5
Elements:

Growing capacity to 10
Growing capacity to 20
=== After adding 5 elements ===
Size: 5, Capacity: 20
Elements: 10 20 30 40 50

=== After adding 10 elements ===
Size: 10, Capacity: 20
Elements: 10 20 30 40 50 60 70 80 90 100

=== After adding 15 elements ===
Size: 15, Capacity: 20
Elements: 10 20 30 40 50 60 70 80 90 100 110 120 130 140 150

Memory freed!
```

---

## Quick Reference

| Concept | Code |
|---------|------|
| Create | `int *arr = malloc(capacity * sizeof(int))` |
| Grow | `arr = realloc(arr, new_capacity * sizeof(int))` |
| Strategy | `capacity = capacity * 2` (double) |
| Add | `arr[size++] = value` |
| Free | `free(arr)` |

---

**Edit main.c and run make test!**
