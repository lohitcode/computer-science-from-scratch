#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 10: WHILE LOOPS
    // =====================================================
    // Loops repeat code while a condition is true
    //
    // Remember:
    //   while (condition) { ... }
    //   Always make sure condition can become FALSE!
    // =====================================================

    // Part 1: Count from 1 to 10
    printf("Counting up: ");
    int count = 1;
    while (count <= 10) {
        printf("%d ", count);
        count++;  // Important: increment count!
    }
    printf("\n");

    // Part 2: Count down from 10 to 1
    printf("Counting down: ");
    int countdown = 10;
    while (countdown >= 1) {
        printf("%d ", countdown);
        countdown--;  // Important: decrement countdown!
    }
    printf("\n");

    // Part 3: Keep asking until positive number
    printf("\nNow let's get a positive number:\n");

    int number = 0;  // Start with 0 (not positive)
    while (number <= 0) {
        printf("Enter a positive number: ");
        scanf("%d", &number);

        if (number > 0) {
            printf("Good! You entered: %d\n", number);
        } else {
            printf("That's not positive! Try again.\n");
        }
    }

    // Bonus: Sum of numbers from 1 to 100
    printf("\nBonus: Sum of 1 to 100\n");

    int sum = 0;
    int i = 1;
    while (i <= 100) {
        sum = sum + i;
        i++;
    }
    printf("Sum = %d\n", sum);

    return 0;
}
