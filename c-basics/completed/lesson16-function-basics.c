#include <stdio.h>

// =====================================================
// LESSON 16: FUNCTION BASICS
// =====================================================
// Functions = reusable blocks of code
//
// Key points:
//   1. Functions must be declared BEFORE they're called
//   2. void = returns nothing
//   3. () = means it's a function
// =====================================================

// Function declarations (must come before main!)
void print_stars() {
    printf("*****\n");
}

void print_name() {
    printf("Lohit\n");
}

void print_separator() {
    printf("=====\n");
}

void print_newline() {
    printf("\n");
}

void print_header() {
    printf("========== MY PROGRAM ==========\n");
}

int main() {
    // Call our functions in order
    print_header();
    print_newline();

    print_stars();
    print_name();
    print_stars();

    print_newline();
    print_separator();

    // Call functions multiple times!
    printf("Repeating stars:\n");
    print_stars();
    print_stars();
    print_stars();

    return 0;
}
