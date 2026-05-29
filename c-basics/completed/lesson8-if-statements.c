#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 8: IF STATEMENTS
    // =====================================================
    // Control flow - making decisions in your code
    //
    // Remember:
    //   =  (one equal)   = assignment (SET value)
    //   == (two equals)  = comparison (CHECK value)
    // =====================================================

    int age;

    printf("Enter your age: ");
    scanf("%d", &age);

    // Check if can vote (18 or older)
    if (age >= 18) {
        printf("You can vote!\n");
    }

    // Check if can drive (16 or older)
    if (age >= 16) {
        printf("You can drive!\n");
    }

    // Check if senior citizen (65 or older)
    if (age >= 65) {
        printf("You're a senior citizen\n");
    }

    // Check if teenager (between 13 and 19)
    // && means AND - both conditions must be true
    if (age >= 13 && age <= 19) {
        printf("You're a teenager\n");
    }

    // Bonus: What about kids?
    if (age < 13) {
        printf("You're a child\n");
    }

    return 0;
}
