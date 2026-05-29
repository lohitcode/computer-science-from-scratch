#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 11: FOR LOOPS
    // =====================================================
    // for loops are cleaner for counting
    //
    // Syntax:
    //   for (init; condition; increment) { ... }
    //
    // Three parts in one line!
    // =====================================================

    // Part 1: Count from 1 to 10
    printf("Counting 1 to 10: ");
    for (int i = 1; i <= 10; i++) {
        printf("%d ", i);
    }
    printf("\n");

    // Part 2: Print even numbers 0 to 20
    printf("Even numbers 0-20: ");
    for (int i = 0; i <= 20; i += 2) {
        printf("%d ", i);
    }
    printf("\n");

    // Part 3: Count down from 10 to 1
    printf("Counting down: ");
    for (int i = 10; i >= 1; i--) {
        printf("%d ", i);
    }
    printf("\n");

    // Part 4: 5x5 grid (nested loops)
    printf("\n5x5 Grid:\n");
    for (int row = 0; row < 5; row++) {
        for (int col = 0; col < 5; col++) {
            printf("(%d,%d) ", row, col);
        }
        printf("\n");
    }

    // Bonus: Multiplication table
    printf("\nMultiplication table (1-5):\n");
    for (int i = 1; i <= 5; i++) {
        for (int j = 1; j <= 5; j++) {
            printf("%2d ", i * j);
        }
        printf("\n");
    }

    return 0;
}
