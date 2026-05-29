#include <stdio.h>
#include <string.h>

// =====================================================
// LESSON 29: STRUCT POINTERS
// =====================================================
// Pass structs by pointer to avoid copying large data
// Use arrow operator -> to access fields through pointer
//
// ptr->field  is same as  (*ptr).field
// =====================================================

// Define structs
struct Point {
    int x;
    int y;
};

struct Rectangle {
    int width;
    int height;
};

struct Student {
    char name[50];
    int age;
    float gpa;
};

// Move point by dx, dy (modifies original)
void move(struct Point *ptr, int dx, int dy) {
    ptr->x = ptr->x + dx;
    ptr->y = ptr->y + dy;
}

// Scale rectangle by factor
void scale(struct Rectangle *ptr, int factor) {
    ptr->width = ptr->width * factor;
    ptr->height = ptr->height * factor;
}

// Print student info (read-only, const prevents modification)
void print_student(const struct Student *ptr) {
    printf("Name: %s\n", ptr->name);
    printf("Age: %d\n", ptr->age);
    printf("GPA: %.2f\n", ptr->gpa);
}

int main() {
    // Test move
    printf("=== Move Point ===\n");
    struct Point p = {3, 4};
    printf("Before: (%d, %d)\n", p.x, p.y);
    move(&p, 5, 2);
    printf("After: (%d, %d)\n\n", p.x, p.y);

    // Test scale
    printf("=== Scale Rectangle ===\n");
    struct Rectangle rect = {5, 3};
    printf("Before: %dx%d\n", rect.width, rect.height);
    scale(&rect, 2);
    printf("After: %dx%d\n\n", rect.width, rect.height);

    // Test print_student
    printf("=== Print Student ===\n");
    struct Student s = {"Alice", 20, 3.8};
    print_student(&s);

    return 0;
}
