#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 14: ARRAY MEMORY
    // =====================================================
    // Arrays are stored in contiguous memory
    // Each element is placed right next to the previous one
    //
    // %p prints memory addresses (pointers)
    // =====================================================

    // Part 1: Int array (4 bytes per element)
    int arr[5] = {10, 20, 30, 40, 50};

    printf("Int array (each element = 4 bytes):\n");
    printf("Array starts at: %p\n\n", arr);

    for (int i = 0; i < 5; i++) {
        printf("arr[%d] at address %p = %d\n", i, &arr[i], arr[i]);
    }

    // Part 2: Char array (1 byte per element)
    char chars[5] = {'A', 'B', 'C', 'D', 'E'};

    printf("\nChar array (each element = 1 byte):\n");
    printf("Array starts at: %p\n\n", chars);

    for (int i = 0; i < 5; i++) {
        printf("chars[%d] at address %p = %c\n", i, &chars[i], chars[i]);
    }

    // Part 3: Double array (8 bytes per element)
    double doubles[3] = {1.1, 2.2, 3.3};

    printf("\nDouble array (each element = 8 bytes):\n");
    printf("Array starts at: %p\n\n", doubles);

    for (int i = 0; i < 3; i++) {
        printf("doubles[%d] at address %p = %.1f\n", i, &doubles[i], doubles[i]);
    }

    // Part 4: Show array name IS the address
    printf("\nProof that arr = &arr[0]:\n");
    printf("arr      = %p\n", arr);
    printf("&arr[0]  = %p\n", &arr[0]);
    printf("Same? %s\n", arr == &arr[0] ? "YES!" : "NO");

    return 0;
}
