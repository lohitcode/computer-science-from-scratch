#include <stdio.h>

// =====================================================
// LESSON 26: FUNCTION POINTERS
// =====================================================
// Pointers that store function addresses
// Allow passing functions as arguments, storing functions in arrays
//
// Syntax: return_type (*name)(params)
// Example: int (*func)(int, int)
// =====================================================

// Operation functions
int add(int a, int b) {
    return a + b;
}

int sub(int a, int b) {
    return a - b;
}

int mul(int a, int b) {
    return a * b;
}

// Function that takes a function pointer
int operate(int a, int b, int (*op)(int, int)) {
    return op(a, b);  // Call whatever function was passed
}

int main() {
    int x = 10, y = 3;

    // Test operate with different functions
    printf("=== Function Pointers ===\n");
    printf("operate(%d, %d, add) = %d\n", x, y, operate(x, y, add));
    printf("operate(%d, %d, sub) = %d\n", x, y, operate(x, y, sub));
    printf("operate(%d, %d, mul) = %d\n", x, y, operate(x, y, mul));

    // Array of function pointers
    printf("\n=== Function Pointer Array ===\n");
    int (*ops[3])(int, int) = {add, sub, mul};
    char *names[] = {"add", "sub", "mul"};

    for (int i = 0; i < 3; i++) {
        printf("%s(%d, %d) = %d\n", names[i], x, y, ops[i](x, y));
    }

    return 0;
}
