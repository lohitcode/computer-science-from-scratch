#include <stdio.h>

// =====================================================
// LESSON 30: TYPEDEF AND STRUCTS
// =====================================================
// typedef creates an alias for a type
// Makes struct code cleaner by removing "struct" keyword
//
// Without typedef:  struct Point p;
// With typedef:     Point p;
// =====================================================

// Define Point with typedef
typedef struct Point {
    int x;
    int y;
} Point;

// Define Rectangle with typedef
typedef struct Rectangle {
    int width;
    int height;
} Rectangle;

// Function using typedef (cleaner!)
Point create_point(int x, int y) {
    Point p;
    p.x = x;
    p.y = y;
    return p;
}

// Pointer parameter with typedef
void move(Point *p, int dx, int dy) {
    p->x = p->x + dx;
    p->y = p->y + dy;
}

// Const pointer with typedef
void print_point(const Point *p) {
    printf("(%d, %d)\n", p->x, p->y);
}

int main() {
    // Notice: no "struct" keyword needed!
    Point p1 = create_point(3, 4);
    Point p2 = {10, 20};

    printf("=== Point 1 ===\n");
    print_point(&p1);

    printf("=== Point 2 ===\n");
    print_point(&p2);

    printf("=== Move Point 1 ===\n");
    move(&p1, 5, 2);
    print_point(&p1);

    // Rectangle with typedef
    Rectangle rect = {5, 3};
    printf("\n=== Rectangle ===\n");
    printf("Size: %dx%d\n", rect.width, rect.height);

    return 0;
}
