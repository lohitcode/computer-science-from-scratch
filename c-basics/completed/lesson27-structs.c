#include <stdio.h>
#include <math.h>

// =====================================================
// LESSON 27: WHAT ARE STRUCTS?
// =====================================================
// Structs group related variables into a single type
// Access fields with dot operator: struct.field
//
// Use for: real-world objects with multiple properties
// =====================================================

// Define Point struct - groups x and y coordinates
struct Point {
    int x;
    int y;
};

// Calculate distance from origin (0,0) using Pythagorean theorem
double distance_from_origin(struct Point p) {
    return sqrt(p.x * p.x + p.y * p.y);
}

// Print point in (x, y) format
void print_point(struct Point p) {
    printf("(%d, %d)", p.x, p.y);
}

int main() {
    // Test Point struct
    printf("=== Point Struct ===\n");

    struct Point p1 = {3, 4};
    printf("Point ");
    print_point(p1);
    printf(" distance: %.2f\n", distance_from_origin(p1));

    struct Point p2 = {0, 0};
    printf("Point ");
    print_point(p2);
    printf(" distance: %.2f\n", distance_from_origin(p2));

    struct Point p3 = {-3, -4};
    printf("Point ");
    print_point(p3);
    printf(" distance: %.2f\n", distance_from_origin(p3));

    return 0;
}
