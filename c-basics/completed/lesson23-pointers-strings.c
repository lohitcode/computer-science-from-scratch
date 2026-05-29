#include <stdio.h>

// =====================================================
// LESSON 23: POINTERS AND STRINGS
// =====================================================
// Strings are arrays of characters ending with '\0'
// We can use pointers to traverse and manipulate them
//
// Key: char *str can access string character by character
// *str gives current character, str++ moves to next
// =====================================================

// Return length of string using pointer traversal
int string_length(char *str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}

// Copy src to dest (assume dest has enough space)
void string_copy(char *dest, char *src) {
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';  // Add null terminator
}

// Compare two strings: 0=equal, -1=s1<s2, 1=s1>s2
int string_compare(char *s1, char *s2) {
    while (*s1 && *s2 && *s1 == *s2) {
        s1++;
        s2++;
    }

    if (*s1 == *s2) return 0;     // Equal
    if (*s1 < *s2) return -1;     // s1 comes before s2
    return 1;                     // s1 comes after s2
}

int main() {
    // Test string_length
    printf("=== String Length ===\n");
    printf("Length of 'Hello': %d\n", string_length("Hello"));
    printf("Length of '': %d\n\n", string_length(""));

    // Test string_copy
    printf("=== String Copy ===\n");
    char dest[20];
    string_copy(dest, "Copy this!");
    printf("Copied: %s\n\n", dest);

    // Test string_compare
    printf("=== String Compare ===\n");
    printf("'apple' vs 'apple': %d\n", string_compare("apple", "apple"));
    printf("'apple' vs 'banana': %d\n", string_compare("apple", "banana"));
    printf("'zebra' vs 'apple': %d\n", string_compare("zebra", "apple"));

    return 0;
}
