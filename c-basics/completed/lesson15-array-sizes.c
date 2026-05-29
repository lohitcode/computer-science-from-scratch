#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 15: ARRAY SIZES
    // =====================================================
    // sizeof returns bytes
    // Array length = sizeof(array) / sizeof(array[0])
    // =====================================================

    // Part 1: Compare different types
    int ints[5] = {1, 2, 3, 4, 5};
    char chars[5] = {'A', 'B', 'C', 'D', 'E'};
    double doubles[5] = {1.1, 2.2, 3.3, 4.4, 5.5};

    printf("Size comparison:\n");
    printf("int array:    %zu bytes, %d elements\n", sizeof(ints), (int)(sizeof(ints) / sizeof(ints[0])));
    printf("char array:   %zu bytes, %d elements\n", sizeof(chars), (int)(sizeof(chars) / sizeof(chars[0])));
    printf("double array: %zu bytes, %d elements\n\n", sizeof(doubles), (int)(sizeof(doubles) / sizeof(doubles[0])));

    // Part 2: Use calculated length
    int numbers[] = {10, 20, 30, 40, 50};
    int length = sizeof(numbers) / sizeof(numbers[0]);

    printf("Array with calculated length:\n");
    for (int i = 0; i < length; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");

    // Part 3: Sum using length
    int sum = 0;
    for (int i = 0; i < length; i++) {
        sum += numbers[i];
    }
    printf("Sum: %d\n", sum);

    // Part 4: Works even if we don't specify size!
    int auto_sized[] = {100, 200, 300};
    int auto_len = sizeof(auto_sized) / sizeof(auto_sized[0]);
    printf("\nAuto-sized array: %d elements\n", auto_len);

    for (int i = 0; i < auto_len; i++) {
        printf("%d ", auto_sized[i]);
    }
    printf("\n");

    return 0;
}
