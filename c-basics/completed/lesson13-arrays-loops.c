#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 13: ARRAYS AND LOOPS
    // =====================================================
    // Arrays + Loops = Perfect combination!
    //
    // Pattern: for (int i = 0; i < size; i++)
    // =====================================================

    int numbers[5] = {12, 45, 67, 23, 89};

    // Part 1: Print all elements using loop
    printf("Array: ");
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // Part 2: Calculate sum using loop
    int sum = 0;
    for (int i = 0; i < 5; i++) {
        sum = sum + numbers[i];
    }
    printf("Sum: %d\n", sum);

    // Part 3: Find maximum
    int max = numbers[0];
    for (int i = 1; i < 5; i++) {
        if (numbers[i] > max) {
            max = numbers[i];
        }
    }
    printf("Maximum: %d\n", max);

    // Part 4: Find minimum
    int min = numbers[0];
    for (int i = 1; i < 5; i++) {
        if (numbers[i] < min) {
            min = numbers[i];
        }
    }
    printf("Minimum: %d\n", min);

    // Part 5: Count even numbers
    int even_count = 0;
    for (int i = 0; i < 5; i++) {
        if (numbers[i] % 2 == 0) {
            even_count++;
        }
    }
    printf("Even numbers: %d\n", even_count);

    return 0;
}
