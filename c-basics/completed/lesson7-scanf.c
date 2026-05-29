#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 7: INPUT WITH scanf
    // =====================================================
    // scanf reads input FROM the keyboard
    // printf sends output TO the screen
    //
    // IMPORTANT: Use & for numbers/chars, NOT for strings!
    // =====================================================

    // Variables to store user input
    char name[50];
    int age;
    float height;

    // Get name
    printf("What is your name? ");
    scanf("%s", name);  // NO & for strings!

    // Get age
    printf("How old are you? ");
    scanf("%d", &age);   // MUST use & for numbers

    // Get height
    printf("Your height (feet, like 5.9)? ");
    scanf("%f", &height);

    // Print everything back
    printf("\nHello %s!\n", name);
    printf("You are %d years old\n", age);
    printf("Your height: %.1f feet\n", height);

    return 0;
}
