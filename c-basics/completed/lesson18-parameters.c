#include <stdio.h>

// =====================================================
// LESSON 18: PARAMETERS
// =====================================================
// Parameters = input values for functions
// Make functions flexible and reusable
//
// PARAMETER = variable in definition
// ARGUMENT  = actual value passed
// =====================================================

// Function with parameters - print a box of stars
void print_box(int width, int height) {
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            printf("*");
        }
        printf("\n");
    }
}

// Function with parameters - calculate power
int power(int base, int exponent) {
    int result = 1;
    for (int i = 0; i < exponent; i++) {
        result = result * base;
    }
    return result;
}

// Function with multiple parameters - find max of three
int max_of_three(int a, int b, int c) {
    int max = a;
    if (b > max) {
        max = b;
    }
    if (c > max) {
        max = c;
    }
    return max;
}

// Function with array parameter
void print_array(int arr[], int size) {
    printf("Array: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Function with string parameter
void greet_person(char name[], int age) {
    printf("Hello %s, you are %d years old!\n", name, age);
}

int main() {
    // Test print_box with different sizes
    printf("3x5 box:\n");
    print_box(5, 3);

    printf("\n2x10 box:\n");
    print_box(10, 2);

    // Test power
    printf("\nPowers:\n");
    printf("2^3 = %d\n", power(2, 3));
    printf("5^2 = %d\n", power(5, 2));
    printf("10^4 = %d\n", power(10, 4));

    // Test max_of_three
    printf("\nMaximums:\n");
    printf("Max of 5, 9, 3 = %d\n", max_of_three(5, 9, 3));
    printf("Max of 100, 50, 75 = %d\n", max_of_three(100, 50, 75));

    // Test array parameter
    int numbers[] = {10, 20, 30, 40, 50};
    printf("\n");
    print_array(numbers, 5);

    // Test string parameter
    printf("\n");
    greet_person("Alice", 25);
    greet_person("Bob", 30);

    return 0;
}
