#include <stdio.h>

// =====================================================
// LESSON 28: STRUCTS AND FUNCTIONS
// =====================================================
// Structs can be passed to and returned from functions
// By default, structs are PASSED BY VALUE (copied)
//
// For small structs, copying is fine
// For large structs, use pointers (next lesson!)
// =====================================================

// Define Rectangle struct
struct Rectangle {
    int width;
    int height;
};

// Create and return a rectangle
struct Rectangle create_rect(int w, int h) {
    struct Rectangle r;
    r.width = w;
    r.height = h;
    return r;
}

// Calculate area (read-only, pass by value is fine for small structs)
int area(struct Rectangle r) {
    return r.width * r.height;
}

// Calculate perimeter
int perimeter(struct Rectangle r) {
    return 2 * (r.width + r.height);
}

// Print rectangle info
void print_rect(struct Rectangle r) {
    printf("Rectangle: %dx%d\n", r.width, r.height);
    printf("Area: %d\n", area(r));
    printf("Perimeter: %d\n", perimeter(r));
}

int main() {
    // Test create_rect
    printf("=== Create Rectangle ===\n");
    struct Rectangle rect = create_rect(5, 3);
    printf("Created: %dx%d\n\n", rect.width, rect.height);

    // Test area
    printf("=== Area ===\n");
    printf("Area: %d\n\n", area(rect));

    // Test perimeter
    printf("=== Perimeter ===\n");
    printf("Perimeter: %d\n\n", perimeter(rect));

    // Test print_rect
    printf("=== Print Rectangle ===\n");
    print_rect(rect);

    return 0;
}
