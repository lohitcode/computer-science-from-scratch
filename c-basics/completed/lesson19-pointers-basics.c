#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 19: WHAT ARE POINTERS?
    // =====================================================
    // Pointer = variable that stores a MEMORY ADDRESS
    //
    // &  = address-of operator (get address)
    // *  = dereference operator (get value AT address)
    // =====================================================

    // Part 1: Basic pointer usage
    int num = 42;
    int *ptr = &num;  // ptr now holds the ADDRESS of num

    printf("=== Basic Pointer ===\n");
    printf("Value of num: %d\n", num);
    printf("Address of num (&num): %p\n", &num);
    printf("Value in ptr: %p\n", ptr);
    printf("Value AT ptr (*ptr): %d\n\n", *ptr);

    // Part 2: Modifying through pointer
    printf("=== Modifying through pointer ===\n");
    printf("Before: num = %d\n", num);

    *ptr = 100;  // Change value AT the address ptr points to

    printf("After *ptr = 100:\n");
    printf("num = %d\n", num);
    printf("*ptr = %d\n\n", *ptr);

    // Part 3: Multiple pointers to same variable
    int *ptr2 = &num;  // Another pointer to num
    int *ptr3 = &num;  // Yet another pointer to num

    printf("=== Multiple pointers ===\n");
    printf("num: %d\n", num);
    printf("*ptr: %d\n", *ptr);
    printf("*ptr2: %d\n", *ptr2);
    printf("*ptr3: %d\n\n", *ptr3);

    // Part 4: Pointer size
    printf("=== Pointer Size ===\n");
    printf("Size of int: %zu bytes\n", sizeof(int));
    printf("Size of pointer (int*): %zu bytes\n", sizeof(int*));
    printf("Size of pointer (char*): %zu bytes\n", sizeof(char*));
    printf("All pointers are same size (addresses)!\n\n");

    // Part 5: NULL pointer
    int *null_ptr = NULL;
    printf("=== NULL Pointer ===\n");
    printf("null_ptr value: %p\n", null_ptr);
    // printf("%d", *null_ptr);  // CRASH! Don't dereference NULL!

    return 0;
}
