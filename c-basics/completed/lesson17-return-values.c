#include <stdio.h>

// =====================================================
// LESSON 17: RETURN VALUES
// =====================================================
// Functions can send back values to the caller
//
// return_type function_name() {
//     return value;
// }
// =====================================================

// Function that returns a sum
int add(int a, int b) {
    return a + b;
}

// Function that returns the square
int square(int num) {
    return num * num;
}

// Function that returns 1 if even, 0 if odd
int is_even(int num) {
    if (num % 2 == 0) {
        return 1;  // Even
    } else {
        return 0;  // Odd
    }
}

// Function that returns maximum of two numbers
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

int main() {
    // Using add() - we get the RETURN VALUE
    int sum = add(5, 3);
    printf("5 + 3 = %d\n", sum);

    // Using square()
    int sq = square(4);
    printf("4 squared = %d\n", sq);

    // Using is_even()
    printf("Is 7 even? %s\n", is_even(7) ? "Yes" : "No");
    printf("Is 8 even? %s\n", is_even(8) ? "Yes" : "No");

    // Using max()
    int maximum = max(10, 25);
    printf("Max of 10 and 25 = %d\n", maximum);

    // Combining functions!
    printf("Square of sum: %d\n", square(add(3, 4)));

    // Return value used in condition
    if (is_even(100)) {
        printf("100 is even!\n");
    }

    return 0;
}
