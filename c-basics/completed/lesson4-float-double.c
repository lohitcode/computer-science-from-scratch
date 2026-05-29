#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 4: FLOAT AND DOUBLE
    // =====================================================
    // Decimal numbers in C
    //
    // float  = 4 bytes, ~7 digits of precision
    // double = 8 bytes, ~15 digits of precision
    // %.2f   = print with 2 decimal places
    // =====================================================

    // Part 1: Circle area calculation
    // Formula: area = pi × radius × radius

    double radius = 5.0;
    double pi = 3.14159;
    double area = pi * radius * radius;

    printf("Circle with radius: %.2f\n", radius);
    printf("Area: %.2f\n\n", area);

    // Part 2: Temperature conversion
    // Formula: F = (C × 9/5) + 32

    double celsius = 25.0;
    double fahrenheit = (celsius * 9.0 / 5.0) + 32.0;

    printf("%.1f°C = %.1f°F\n", celsius, fahrenheit);

    return 0;
}
