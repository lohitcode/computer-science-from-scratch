#include <stdio.h>

int main() {
    // =====================================================
    // LESSON 3: VARIABLES AND int
    // =====================================================
    // Your task: Create variables for a game character
    //
    // Remember: int = integer (whole number)
    //           %d = placeholder for printing integers
    // =====================================================

    // TODO: Declare three integer variables
    int score = 0;
    int lives = 3;
    int level = 1;

    // TODO: Print initial values
    printf("Game Started:\n");
    printf("Score: %d, Lives: %d, Level: %d\n\n", score, lives, level);

    // TODO: Change the values (player made progress!)
    score = 100;
    lives = 2;
    level = 2;

    // TODO: Print new values
    printf("After playing:\n");
    printf("Score: %d, Lives: %d, Level: %d\n", score, lives, level);

    return 0;
}
