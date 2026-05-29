#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 12: ARRAY BASICS
    // =====================================================
    // Array = collection of same-type values
    // Index starts at 0, not 1!
    // =====================================================

    // Part 1: Create and access array elements
    int numbers[5] = {10, 20, 30, 40, 50};

    printf("Array elements:\n");
    printf("Index 0: %d\n", numbers[0]);
    printf("Index 1: %d\n", numbers[1]);
    printf("Index 2: %d\n", numbers[2]);
    printf("Index 3: %d\n", numbers[3]);
    printf("Index 4: %d\n", numbers[4]);

    // Part 2: Calculate sum
    int sum = numbers[0] + numbers[1] + numbers[2] + numbers[3] + numbers[4];
    printf("\nSum: %d\n", sum);

    // Part 3: Different array types
    char grades[3] = {'A', 'B', 'C'};
    printf("\nGrades:\n");
    printf("First grade: %c\n", grades[0]);
    printf("Last grade: %c\n", grades[2]);

    // Part 4: Array of floats
    float temperatures[3] = {98.6, 99.2, 97.5};
    printf("\nTemperatures:\n");
    printf("Temp 1: %.1f\n", temperatures[0]);
    printf("Temp 2: %.1f\n", temperatures[1]);
    printf("Temp 3: %.1f\n", temperatures[2]);

    return 0;
}
