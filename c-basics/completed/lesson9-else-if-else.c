#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 9: ELSE IF AND ELSE
    // =====================================================
    // else if = check another condition if previous was false
    // else = catch-all if no conditions were true
    //
    // IMPORTANT: Only ONE block runs!
    // =====================================================

    int score;

    printf("Enter your score (0-100): ");
    scanf("%d", &score);

    // Grade calculator using else if
    if (score >= 90) {
        printf("Grade: A - Excellent!\n");
    } else if (score >= 80) {
        printf("Grade: B - Good job!\n");
    } else if (score >= 70) {
        printf("Grade: C - Okay\n");
    } else if (score >= 60) {
        printf("Grade: D - Passing\n");
    } else {
        printf("Grade: F - Need to study more!\n");
    }

    // Bonus: Temperature example
    printf("\nLet's check temperature:\n");

    int temp;
    printf("Enter temperature: ");
    scanf("%d", &temp);

    if (temp > 30) {
        printf("It's hot!\n");
    } else if (temp > 20) {
        printf("It's warm\n");
    } else if (temp > 10) {
        printf("It's cool\n");
    } else {
        printf("It's cold!\n");
    }

    return 0;
}
