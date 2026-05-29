# C Programming Notes - Quick Reference

*Your personal C textbook - filled in as you complete lessons*

---

## Chapter 1: Your First C Program

### ✅ Lesson 1: Hello World

**What is C?**
- Created in 1972 by Dennis Ritchie at Bell Labs
- Used to build operating systems (Linux, Windows, macOS)
- Gives direct control over memory

**Basic C Program Structure:**
```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

**Line-by-line:**
| Line | Meaning |
|------|---------|
| `#include <stdio.h>` | Include standard input/output library |
| `int main() {` | Main function - program starts here |
| `printf("Hello, World!\n");` | Print text to screen |
| `return 0;` | End program successfully |
| `}` | Close main function |

**Key Concepts:**
- Every C program must have `main()` - execution starts here
- `\n` = newline character (moves to next line)
- Statements end with `;`

---

### ✅ Lesson 2: Comments

**What are comments?**
- Notes for humans - computer ignores them
- Used to explain code

**Two types of comments:**
```c
// Single-line comment

/* Multi-line
   comment */
```

**When to use comments:**
- Explain what code does
- Make notes for yourself
- Temporarily disable code

---

## Chapter 2: Variables and Data Types

### ✅ Lesson 3: Variables and int

**What is a variable?**
- A named storage location in memory
- Holds a value that can change

**Declaring an integer variable:**
```c
int age = 25;
```

**Parts:**
- `int` = type (integer, whole number)
- `age` = name (you choose this)
- `25` = value
- `;` = ends the statement

**Common integer types:**
| Type | Size | Range |
|------|------|-------|
| `int` | 4 bytes | -2 billion to +2 billion |
| `short` | 2 bytes | -32,768 to +32,767 |
| `long` | 8 bytes | Very large numbers |

**Assigning new values:**
```c
int score = 0;
score = 100;  // Now score is 100
score = 200;  // Now score is 200
```

**Printing variables:**
```c
int count = 5;
printf("The count is: %d", count);
// Output: The count is: 5
```

**`%d`** = placeholder for an integer

---

### ✅ Lesson 4: float and double

**What are float and double?**
- `float` = decimal numbers with less precision
- `double` = decimal numbers with more precision (double the precision!)

**Why two types?**
- `float` = 4 bytes, ~7 decimal digits of precision
- `double` = 8 bytes, ~15 decimal digits of precision

**Declaring:**
```c
float pi = 3.14f;           // Note the 'f' suffix
double temperature = 98.6;
```

**Printing:**
```c
printf("%f", 3.14159);    // Default: 3.141590
printf("%.2f", 3.14159);  // 2 decimal places: 3.14
printf("%.4f", 3.14159);  // 4 decimal places: 3.1416
```

**The `.` in `%f` = how many decimal places to show**

**Why not just use double always?**
- Uses more memory (matters when you have millions of numbers)
- Slightly slower (rarely matters today)
- In embedded systems, every byte counts!

---

### ✅ Lesson 5: char and ASCII

**What is char?**
- 1 byte = 8 bits = numbers from -128 to 127
- Stores characters using ASCII code
- Characters ARE numbers internally!

**Complete ASCII Table (0-127):**

| Dec | Char | Dec | Char | Dec | Char | Dec | Char | Dec | Char | Dec | Char | Dec | Char | Dec | Char |
|-----|------|-----|------|-----|------|-----|------|-----|------|-----|------|-----|------|-----|------|
| 0 | `NUL` | 16 | `DLE` | 32 | `␣` | 48 | `0` | 64 | `@` | 80 | `P` | 96 | `` ` `` | 112 | `p` |
| 1 | `SOH` | 17 | `DC1` | 33 | `!` | 49 | `1` | 65 | `A` | 81 | `Q` | 97 | `a` | 113 | `q` |
| 2 | `STX` | 18 | `DC2` | 34 | `"` | 50 | `2` | 66 | `B` | 82 | `R` | 98 | `b` | 114 | `r` |
| 3 | `ETX` | 19 | `DC3` | 35 | `#` | 51 | `3` | 67 | `C` | 83 | `S` | 99 | `c` | 115 | `s` |
| 4 | `EOT` | 20 | `DC4` | 36 | `$` | 52 | `4` | 68 | `D` | 84 | `T` | 100 | `d` | 116 | `t` |
| 5 | `ENQ` | 21 | `NAK` | 37 | `%` | 53 | `5` | 69 | `E` | 85 | `U` | 101 | `e` | 117 | `u` |
| 6 | `ACK` | 22 | `SYN` | 38 | `&` | 54 | `6` | 70 | `F` | 86 | `V` | 102 | `f` | 118 | `v` |
| 7 | `BEL` | 23 | `ETB` | 39 | `'` | 55 | `7` | 71 | `G` | 87 | `W` | 103 | `g` | 119 | `w` |
| 8 | `BS` | 24 | `CAN` | 40 | `(` | 56 | `8` | 72 | `H` | 88 | `X` | 104 | `h` | 120 | `x` |
| 9 | `HT` (`\t`) | 25 | `EM` | 41 | `)` | 57 | `9` | 73 | `I` | 89 | `Y` | 105 | `i` | 121 | `y` |
| 10 | `LF` (`\n`) | 26 | `SUB` | 42 | `*` | 58 | `:` | 74 | `J` | 90 | `Z` | 106 | `j` | 122 | `z` |
| 11 | `VT` | 27 | `ESC` | 43 | `+` | 59 | `;` | 75 | `K` | 91 | `[` | 107 | `k` | 123 | `{` |
| 12 | `FF` (`\f`) | 28 | `FS` | 44 | `,` | 60 | `<` | 76 | `L` | 92 | `\` | 108 | `l` | 124 | `|` |
| 13 | `CR` (`\r`) | 29 | `GS` | 45 | `-` | 61 | `=` | 77 | `M` | 93 | `]` | 109 | `m` | 125 | `}` |
| 14 | `SO` | 30 | `RS` | 46 | `.` | 62 | `>` | 78 | `N` | 94 | `^` | 110 | `n` | 126 | `~` |
| 15 | `SI` | 31 | `US` | 47 | `/` | 63 | `?` | 79 | `O` | 95 | `_` | 111 | `o` | 127 | `DEL` |

**Control Characters (0-31, 127) - What they do:**

| Code | Decimal | Description | Use in C |
|------|---------|-------------|----------|
| `NUL` | 0 | Null character | String terminator `\0` |
| `BEL` | 7 | Bell/Audible alert | Makes beep sound |
| `BS` | 8 | Backspace | Move cursor back `\b` |
| `HT` | 9 | Horizontal Tab | Tab to next position `\t` |
| `LF` | 10 | Line Feed | New line on Unix/Linux `\n` |
| `VT` | 11 | Vertical Tab | Move down one line |
| `FF` | 12 | Form Feed | Page break/eject printer `\f` |
| `CR` | 13 | Carriage Return | Return to start of line `\r` |
| `ESC` | 27 | Escape | Escape key |
| `DEL` | 127 | Delete | Delete character |

**Escape Sequences in C:**
- `\0` = NUL (0)
- `\n` = Newline (10)
- `\t` = Tab (9)
- `\r` = Carriage return (13)
- `\\` = Backslash (92)
- `\"` = Double quote (34)
- `\'` = Single quote (39)
- `\%` = Percent sign (37)

**Quick Reference:**
- Digits `'0'-'9'` = 48-57
- Uppercase `'A'-'Z'` = 65-90
- Lowercase `'a'-'z'` = 97-122
- Space ` ` = 32

**Characters = Numbers:**
```c
char c1 = 'A';     // Stores 65
char c2 = 65;      // Also stores 'A'!

printf("%c", c1);  // Output: A  (print as character)
printf("%d", c2);  // Output: 65 (print as number)

// Same works with int
int i = 'A';       // int can store 65 too
printf("%c", i);   // Output: A
```

---

## Chapter 2 Summary: All Data Types

**Complete Data Types Reference:**

| Type | Bytes | Bits | Range | Can store numbers? | Can store characters? |
|------|-------|------|-------|-------------------|----------------------|
| `char` | 1 | 8 | -128 to 127 | ✅ Yes | ✅ Yes (ASCII) |
| `short` | 2 | 16 | -32,768 to 32,767 | ✅ Yes | ❌ No |
| `int` | 4 | 32 | ±2 billion | ✅ Yes | ❌ No* |
| `long` | 8 | 64 | Huge numbers | ✅ Yes | ❌ No* |
| `float` | 4 | 32 | ~7 digit precision | ✅ Yes | ❌ No |
| `double` | 8 | 64 | ~15 digit precision | ✅ Yes | ❌ No |

\* `int` and `long` CAN store ASCII numbers (65, 66, etc.) and print with `%c`, but it's wasteful (4-8 bytes for 1 byte of data).

**Printf Format Specifiers:**

| Type | Format Specifier | Example |
|------|------------------|---------|
| `char` | `%c` or `%d` | `printf("%c", c)` |
| `short` | `%d` or `%hd` | `printf("%d", s)` |
| `int` | `%d` or `%i` | `printf("%d", i)` |
| `long` | `%ld` | `printf("%ld", l)` |
| `float` | `%f` | `printf("%.2f", f)` |
| `double` | `%lf` or `%f` | `printf("%.2lf", d)` |

**When to use each:**
- `char` - Single characters, small numbers (-128 to 127)
- `short` - Small whole numbers, saves memory
- `int` - Default for whole numbers
- `long` - Very large numbers
- `float` - Decimals when memory matters
- `double` - Decimals when precision matters

---

## Chapter 3: Input and Output

### ✅ Lesson 6: printf (Output)

**What is printf?**
- Stands for "print formatted"
- Sends output to the screen (terminal)
- Most used function in C!

**Syntax:**
```c
printf("format string", variables...);
```

**Format Specifiers:**
| Code | Type | Example |
|------|------|---------|
| `%d` | int | `printf("%d", age);` |
| `%f` | double | `printf("%.2f", pi);` |
| `%c` | char | `printf("%c", letter);` |
| `%s` | string | `printf("%s", name);` |

**Escape Sequences:**
| Code | Meaning |
|------|---------|
| `\n` | Newline |
| `\t` | Tab |
| `\\` | Backslash |
| `\"` | Double quote |
| `%%` | Percent sign |

---

### ✅ Lesson 7: scanf (Input)

**What is scanf?**
- Stands for "scan formatted"
- Reads input from the keyboard
- The opposite of printf!

**Syntax:**
```c
scanf("format", &variable);
           ^        ^
           |        |
           format    MUST use & for numbers/chars!
```

**The `&` is crucial!**
```c
int age;
scanf("%d", &age);   // ✅ Correct - reads into age
scanf("%d", age);    // ❌ WRONG - will crash!
```

**`&` means "address of"** - tells scanf WHERE to store the input.

**Reading different types:**
```c
int number;
scanf("%d", &number);

float temperature;
scanf("%f", &temperature);

double precision;
scanf("%lf", &precision);  // Note: %lf for double

char letter;
scanf("%c", &letter);
```

**Important: scanf skips newlines!**
```c
int age;
char name[50];

scanf("%d", &age);        // Reads age, leaves \n in buffer
scanf("%s", name);        // Skips the \n, works fine
```

**Common gotcha: char vs string**
```c
char letter;
scanf("%c", &letter);     // Single char - use &

char name[50];
scanf("%s", name);        // String - NO & (name is already an address!)
```

---

## Chapter 4: Control Flow

### ✅ Lesson 8: if statements

**What is control flow?**
- Making decisions in your code
- Running different code based on conditions
- "If this is true, do this"

**Basic if statement:**
```c
if (condition) {
    // Code runs ONLY if condition is true
}
```

**Comparison operators:**
| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `if (age == 18)` |
| `!=` | Not equal to | `if (age != 18)` |
| `<` | Less than | `if (age < 18)` |
| `>` | Greater than | `if (age > 18)` |
| `<=` | Less or equal | `if (age <= 18)` |
| `>=` | Greater or equal | `if (age >= 18)` |

**IMPORTANT: One `=` vs Two `==`**
```c
if (age = 18) { }   // ❌ WRONG - assigns 18 to age!
if (age == 18) { }  // ✅ CORRECT - checks if age equals 18
```

**True vs False in C:**
- `0` = false
- Any non-zero = true (1, -5, 100, etc.)

```c
if (1)   printf("This runs\n");    // 1 = true
if (0)   printf("This skips\n");   // 0 = false
if (-5)  printf("This runs\n");    // non-zero = true
```

---

### ✅ Lesson 9: else if and else

**else if - multiple conditions:**
```c
if (condition1) {
    // Runs if condition1 is true
} else if (condition2) {
    // Runs if condition1 is false AND condition2 is true
} else {
    // Runs if ALL conditions are false
}
```

**Example - Grade calculator:**
```c
int score = 85;

if (score >= 90) {
    printf("Grade: A\n");
} else if (score >= 80) {
    printf("Grade: B\n");  // This runs
} else if (score >= 70) {
    printf("Grade: C\n");
} else {
    printf("Grade: F\n");
}
```

**Nested if:**
```c
if (age >= 18) {
    if (has_license) {
        printf("Can drive\n");
    } else {
        printf("Need license\n");
    }
} else {
    printf("Too young to drive\n");
}
```

---

## Chapter 5: Loops

### ✅ Lesson 10: while loops

**What is a loop?**
- Repeat code multiple times
- Don't write the same code over and over

**while loop syntax:**
```c
while (condition) {
    // Code repeats while condition is true
}
```

**Basic example:**
```c
int count = 0;

while (count < 5) {
    printf("Count: %d\n", count);
    count++;  // Important: increase count!
}

printf("Done!\n");
```

**WARNING: Infinite loops!**
```c
int count = 0;

while (count < 5) {
    printf("Count: %d\n", count);
    // Oops! Forgot count++ - runs forever!
}
```

**Real-world example:**
```c
// Keep asking until valid input
int age;
while (1) {  // 1 = always true, infinite loop
    printf("Enter age (0-120): ");
    scanf("%d", &age);

    if (age >= 0 && age <= 120) {
        break;  // Exit the loop
    }

    printf("Invalid age! Try again.\n");
}
```

---

### ✅ Lesson 11: for loops

**for loop syntax:**
```c
for (initialization; condition; increment) {
    // Code repeats
}
```

**Example:**
```c
for (int i = 0; i < 5; i++) {
    printf("Count: %d\n", i);
}
```

**Breakdown:**
| Part | What happens | When |
|------|--------------|------|
| `int i = 0` | Set i to 0 | Once, at start |
| `i < 5` | Check condition | Every iteration |
| `i++` | Increase i by 1 | After each iteration |

**while vs for:**
```c
// while loop - more flexible
int i = 0;
while (i < 5) {
    printf("%d\n", i);
    i++;
}

// for loop - cleaner for counting
for (int i = 0; i < 5; i++) {
    printf("%d\n", i);
}
```

**Counting patterns:**
```c
// Count up: 0 to 4
for (int i = 0; i < 5; i++)

// Count down: 4 to 0
for (int i = 4; i >= 0; i--)

// Count by 2: 0, 2, 4, 6, 8
for (int i = 0; i < 10; i += 2)
```

**Nested loops:**
```c
for (int row = 0; row < 3; row++) {
    for (int col = 0; col < 3; col++) {
        printf("(%d,%d) ", row, col);
    }
    printf("\n");
}
```

Output:
```
(0,0) (0,1) (0,2)
(1,0) (1,1) (1,2)
(2,0) (2,1) (2,2)
```

---

## Chapter 6: Arrays

### ✅ Lesson 12: Array Basics

**What is an array?**
- A collection of values of the SAME type
- Stored in contiguous (side-by-side) memory
- Accessed by index starting at 0

**Declaring an array:**
```c
int numbers[5];              // Array of 5 integers
int scores[3] = {90, 85, 95}; // Array with initial values
char name[50];                // Array of 50 characters
```

**Accessing elements:**
```c
int scores[3] = {90, 85, 95};

printf("%d", scores[0]);  // 90 (first element)
printf("%d", scores[1]);  // 85 (second element)
printf("%d", scores[2]);  // 95 (third element)
```

**Index starts at 0, not 1!**
```
Array: [90 | 85 | 95]
Index:   0   1   2
```

**Memory layout:**
```
int scores[3] = {90, 85, 95};

Memory (each int = 4 bytes):
0x1000: [ 90 ]  ← scores[0]
0x1004: [ 85 ]  ← scores[1]
0x1008: [ 95 ]  ← scores[2]
```

**Array size:**
```c
int arr[5];           // Can hold 5 integers
arr[0] = 10;          // First element
arr[4] = 50;          // Last element
// arr[5] = 60;       // ❌ OUT OF BOUNDS! Only 0-4
```

---

### ✅ Lesson 13: Arrays and Loops

**Why combine arrays and loops?**
Arrays and loops are perfect together!

```
WITHOUT loop (tedious):
printf("%d\n", arr[0]);
printf("%d\n", arr[1]);
printf("%d\n", arr[2]);
printf("%d\n", arr[3]);
printf("%d\n", arr[4]);

WITH loop (clean):
for (int i = 0; i < 5; i++) {
    printf("%d\n", arr[i]);
}
```

**The pattern:**
```c
for (int i = 0; i < size; i++) {
    // Use arr[i]
}
```

**Example: Print all elements**
```c
int scores[5] = {90, 85, 95, 88, 92};

for (int i = 0; i < 5; i++) {
    printf("Score %d: %d\n", i, scores[i]);
}
```

**Example: Sum of array**
```c
int numbers[5] = {10, 20, 30, 40, 50};
int sum = 0;

for (int i = 0; i < 5; i++) {
    sum = sum + numbers[i];  // Add each element
}

printf("Sum: %d\n", sum);  // 150
```

**Example: Find maximum**
```c
int scores[5] = {90, 85, 95, 88, 92};
int max = scores[0];  // Start with first element

for (int i = 1; i < 5; i++) {
    if (scores[i] > max) {
        max = scores[i];  // Found bigger number
    }
}

printf("Maximum: %d\n", max);  // 95
```

---

### ✅ Lesson 14: Array Memory

**How arrays are stored in memory:**

Arrays are stored in **contiguous memory** - each element is right next to the previous one.

```c
int arr[5] = {10, 20, 30, 40, 50};
```

**Memory layout (each int = 4 bytes):**
```
Address:   Value:        Index:
0x1000  →  [ 10 ]  ←    arr[0]
0x1004  →  [ 20 ]  ←    arr[1]
0x1008  →  [ 30 ]  ←    arr[2]
0x100C  →  [ 40 ]  ←    arr[3]
0x1010  →  [ 50 ]  ←    arr[4]
```

**How `arr[i]` actually works:**
```c
arr[i]  →  *(base_address + i * sizeof(int))

Example:
arr[2]  →  *(0x1000 + 2 * 4)  →  *(0x1008)  →  30
```

**Array name IS an address:**
```c
int arr[5];

printf("%p", arr);    // Address of first element
printf("%p", &arr[0]); // Same thing!

arr[0] = 10;   // Normal access
*arr = 10;     // Same thing (dereference address)
```

---

### ✅ Lesson 15: Array Sizes

**Getting the size of an array:**

```c
int arr[5];

// Total bytes
size_t total_bytes = sizeof(arr);  // 5 × 4 = 20 bytes

// Size of one element
size_t one_element = sizeof(arr[0]);  // 4 bytes

// Number of elements
size_t count = sizeof(arr) / sizeof(arr[0]);  // 20 / 4 = 5
```

**The pattern for array length:**
```c
int length = sizeof(arr) / sizeof(arr[0]);
```

**Using the length in loops:**
```c
int arr[] = {10, 20, 30, 40, 50};
int length = sizeof(arr) / sizeof(arr[0]);

for (int i = 0; i < length; i++) {
    printf("%d ", arr[i]);
}
```

**IMPORTANT: sizeof only works for static arrays!**
```c
int* ptr = malloc(5 * sizeof(int));
sizeof(ptr);  // Returns 8 (pointer size), NOT 20!
```

---

## Chapter 7: Functions

### ✅ Lesson 16: Function Basics

**What is a function?**
- A reusable block of code
- Does a specific task
- Can be called multiple times

**Why use functions?**
- Don't repeat yourself (DRY)
- Organize code into logical parts
- Easier to debug and maintain

**Function syntax:**
```c
return_type function_name(parameters) {
    // Code to execute
    return value;  // Optional
}
```

**Simple function example:**
```c
void say_hello() {
    printf("Hello, World!\n");
}

int main() {
    say_hello();  // Call the function
    return 0;
}
```

**Function parts:**
| Part | Purpose | Example |
|------|---------|---------|
| `return_type` | What the function returns | `void`, `int`, `float` |
| `function_name` | Name to call it | `say_hello` |
| `parameters` | Input values (optional) | `(int x, int y)` |
| `body` | Code inside `{ }` | `{ printf("Hi"); }` |
| `return` | Send back a value | `return 0;` |

**void = returns nothing:**
```c
void print_message() {
    printf("This is a message\n");
    // No return needed
}
```

---

### ✅ Lesson 17: Return Values

**What is a return value?**
- A value that a function sends back to the caller
- The "result" of the function

**Functions that return values:**
```c
int add() {
    int result = 5 + 3;
    return result;  // Send back 8
}

int main() {
    int value = add();  // value becomes 8
    printf("%d", value);  // Prints 8
}
```

**Return types:**
| Type | Meaning | Example |
|------|---------|---------|
| `void` | Returns nothing | `void print_msg()` |
| `int` | Returns integer | `int get_age()` |
| `float` | Returns decimal | `float get_pi()` |
| `char` | Returns character | `char get_grade()` |
| `double` | Returns precise decimal | `double calculate()` |

**Once return runs, function ENDS:**
```c
int test() {
    return 5;
    printf("Never runs!\n");  // Dead code
}
```

---

### ✅ Lesson 18: Parameters

**What are parameters?**
- Input values that you pass INTO a function
- Make functions flexible and reusable

**Function with parameters:**
```c
void greet_person(char name[]) {
    printf("Hello, %s!\n", name);
}

int main() {
    greet_person("Alice");  // Prints: Hello, Alice!
    greet_person("Bob");    // Prints: Hello, Bob!
}
```

**Parameter vs Argument:**
```c
int add(int a, int b) {   // a and b are PARAMETERS
    return a + b;
}

int result = add(5, 3);   // 5 and 3 are ARGUMENTS
```

- **Parameter** = Variable in function definition
- **Argument** = Actual value passed when calling

**Pass by value (important!):**
```c
void try_to_change(int x) {
    x = 999;  // Only changes the COPY
}

int main() {
    int num = 5;
    try_to_change(num);
    printf("%d", num);  // Still 5! Original unchanged
}
```

**Array parameters (special case):**
```c
void print_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
}

int numbers[] = {1, 2, 3, 4, 5};
print_array(numbers, 5);
```

---

## Chapter 8: Pointers

### ✅ Lesson 19: What are Pointers?

**What is a pointer?**
- A variable that STORES A MEMORY ADDRESS
- Points to another variable
- One of C's most powerful (and confusing!) features

**Basic syntax:**
```c
int num = 42;      // Regular variable
int *ptr = &num;   // Pointer variable (stores address of num)
```

**The two operators:**
| Operator | Name | What it does |
|----------|------|--------------|
| `&` | Address-of | Gets the address of a variable |
| `*` | Dereference | Gets the value AT an address |

**Memory picture:**
```
Stack:
┌─────────────────────────────┐
│  num   [ 42 ]    @ 0x1000   │ ← Holds value 42
├─────────────────────────────┤
│  ptr    [ 0x1000 ] @ 0x1008 │ ← Holds ADDRESS of num
└─────────────────────────────┘

ptr "points to" num
```

**Declaration styles (all correct):**
```c
int* ptr1;    // Star next to type
int *ptr2;    // Star next to variable (most common)
int * ptr3;   // Star in middle
```

**Null pointer:**
```c
int *ptr = NULL;  // Points to nothing
// Always initialize pointers to NULL!
```

---

### ✅ Lesson 20: Pointers and Functions

**Problem: Parameters are copies!**

Remember from Lesson 18 - when you pass a variable to a function, C makes a COPY. The function can't modify the original.

**Solution: Pass pointers!**

If you pass a POINTER, the function can modify the original variable.

```c
void actually_change(int *ptr) {
    *ptr = 999;  // Modifies the ORIGINAL variable
}

int main() {
    int num = 5;
    actually_change(&num);  // Pass ADDRESS
    printf("%d", num);  // Now 999!
}
```

**Swap function (classic example):**
```c
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 5, y = 10;
    swap(&x, &y);
    printf("x=%d, y=%d", x, y);  // x=10, y=5
}
```

**Pattern:**
```c
// Function signature: use pointer type
void modify(int *ptr) { ... }

// Function call: use & to pass address
modify(&variable);
```

---

### ✅ Lesson 21: Pointers and Arrays

**Array names decay to pointers!**

```c
int arr[5] = {10, 20, 30, 40, 50};

// These are IDENTICAL:
arr[0]     ==  *arr       // First element
arr[1]     ==  *(arr+1)   // Second element
```

**Secret:** `arr[i]` is actually `*(arr + i)` in disguise!

**Array vs Pointer differences:**
| | Array | Pointer |
|-|-------|---------|
| `sizeof(arr)` | Total bytes (e.g., 20) | 8 bytes (just address) |
| Reassign | `arr = ptr;` ❌ | `ptr = arr;` ✓ |

---

### ✅ Lesson 22: Pointer Arithmetic

**Adding to pointers moves by sizeof(type), not 1 byte!**

```c
int arr[5] = {10, 20, 30, 40, 50};
int *ptr = arr;

ptr++;      // Moves 4 bytes (to next int)
ptr++;      // Moves 4 bytes more
```

**Operations:**
```c
ptr++;      // Move to next element
ptr--;      // Move to previous element
ptr + n;    // n elements ahead
ptr - n;    // n elements behind
p2 - p1;    // Distance in elements (not bytes!)
```

---

### ✅ Lesson 23: Pointers and Strings

**Strings are char arrays ending with '\0'**

```c
char str[] = "Hello";  // Actually: {'H','e','l','l','o','\0'}
```

**Two ways to create strings:**
```c
char arr[] = "Hello";   // Array on stack, can modify
arr[0] = 'h';           // ✓ Works

char *ptr = "Hello";    // Points to string literal (read-only)
ptr[0] = 'h';           // ✗ CRASH! Cannot modify
```

**Common string function:**
```c
int string_length(char *str) {
    int len = 0;
    while (*str != '\0') {
        len++;
        str++;
    }
    return len;
}
```

---

### ✅ Lesson 24: Const and Pointers

**const means "cannot modify" - read from right to left!**

| Declaration | Read as | Can change *ptr | Can change ptr |
|-------------|---------|-----------------|----------------|
| `int *ptr` | ptr points to int | ✓ | ✓ |
| `const int *ptr` | ptr points to const int | ✗ | ✓ |
| `int *const ptr` | ptr is const pointer to int | ✓ | ✗ |
| `const int *const ptr` | ptr is const to const int | ✗ | ✗ |

**Use in function parameters:**
```c
// Promises: won't modify the array
void print(const int *arr, int size) {
    printf("%d", arr[0]);  // ✓ Reading is fine
}
```

---

### ✅ Lesson 25: Double Pointers

**Pointer to a pointer: int ****

```c
int num = 42;
int *ptr = &num;        // Pointer to int
int **dptr = &ptr;      // Pointer to pointer
```

**Memory chain:**
```
dptr ──→ ptr ──→ num

*dptr  → gets ptr (which is &num)
**dptr → gets num (which is 42)
```

**Pattern:**
| Task | Signature | Call |
|------|-----------|------|
| Modify value | `void func(int *ptr)` | `func(&var)` |
| Modify pointer | `void func(int **ptr)` | `func(&ptr)` |

---

### ✅ Lesson 26: Function Pointers

**Pointers that store function addresses - call functions through pointers!**

```c
int add(int a, int b) { return a + b; }

int (*func_ptr)(int, int) = add;
int result = func_ptr(5, 3);  // Calls add(5, 3) = 8
```

**Why function pointers?**
- **Callbacks:** Pass function to another function
- **qsort:** `qsort(arr, size, sizeof(int), compare_func)`
- **Jump tables:** Array of functions for fast dispatch

---

## Chapter 8: Pointers - Summary

**Key Takeaways:**
- Pointers store memory addresses
- `&` gets address, `*` dereferences
- Arrays decay to pointers (mostly)
- Pointer arithmetic adds sizeof(type)
- String literals are read-only
- `const` prevents modification
- Double pointers modify pointers
- Function pointers enable callbacks

**When to use pointers:**
- Modify original variables
- Pass arrays to functions
- Work with memory directly
- Build dynamic data structures
- Implement callbacks

---

## Chapter 9: Structs

### ✅ Lesson 27: What are Structs?

**What is a struct?**

Groups related variables into a single custom type.

```c
struct Point {
    int x;
    int y;
};
```

**Creating and using:**
```c
struct Point p1 = {3, 4};    // Initialize
p1.x = 10;                   // Access fields with dot
p1.y = 20;
```

**Memory layout:**
```
struct Point {
    int x;    // 4 bytes
    int y;    // 4 bytes
};

Memory:
┌────┬────┐
│ x  │ y  │  = 8 bytes total
│ 4B │ 4B │
└────┴────┘
```

---

### ✅ Lesson 28: Structs and Functions

**Passing structs to functions**

By default, structs are passed by value (copied):

```c
void print_point(struct Point p) {
    printf("(%d, %d)", p.x, p.y);
}  // p is a COPY
```

**Returning structs:**
```c
struct Point create_point(int x, int y) {
    struct Point p;
    p.x = x;
    p.y = y;
    return p;  // Returns the whole struct
}
```

**Rule of thumb:**
- Small structs (<16 bytes): Pass by value (fine)
- Large structs (>16 bytes): Pass by pointer (next lesson!)

---

### ✅ Lesson 29: Struct Pointers

**Arrow operator `->`**

For accessing struct fields through pointers:

```c
struct Point p = {3, 4};
struct Point *ptr = &p;

ptr->x = 10;  // Same as (*ptr).x = 10
```

**Dot vs Arrow:**
| Code | Meaning |
|------|---------|
| `p.x` | Field of struct variable |
| `ptr->x` | Field of struct that pointer points to |

**Modifying through pointers:**
```c
void move(struct Point *ptr, int dx, int dy) {
    ptr->x = ptr->x + dx;  // Modifies original!
    ptr->y = ptr->y + dy;
}
```

---

### ✅ Lesson 30: Typedef and Structs

**What is typedef?**

Creates an alias (nickname) for a type:

```c
typedef unsigned long ulong;  // "ulong" = "unsigned long"
```

**Typedef with structs:**
```c
typedef struct Point {
    int x;
    int y;
} Point;  // "Point" is now an alias for "struct Point"
```

**Before vs After:**
```c
// Without typedef
struct Point p1;

// With typedef
Point p1;       // Cleaner!
```

---

## Chapter 9: Structs - Summary

**Key Takeaways:**
- Structs group related data
- Access fields with dot operator `.`
- Pass small structs by value, large by pointer
- Arrow operator `->` for pointer access
- `typedef` creates cleaner names

---

## Chapter 10: Dynamic Memory

### ✅ Lesson 31: What is Dynamic Memory?

**Stack vs Heap:**

| Stack | Heap |
|-------|------|
| Automatic allocation | Manual allocation |
| Function scope | Survives until free |
| Limited size (~8MB) | Large size (GBs) |
| Freed automatically | Must free manually |

**Why dynamic memory?**
- Size unknown at compile time
- Data must outlive function
- Large allocations (>1MB)
- Growing data structures

---

### ✅ Lesson 32: malloc and free

**malloc - Allocate memory:**
```c
void *malloc(size_t size);

int *ptr = malloc(5 * sizeof(int));  // 5 integers
```

**free - Release memory:**
```c
void free(void *ptr);

free(ptr);
ptr = NULL;  // Prevent dangling pointer
```

**Complete pattern:**
```c
int *arr = malloc(10 * sizeof(int));

if (arr == NULL) {  // ALWAYS check!
    return 1;
}

arr[0] = 10;  // Use

free(arr);      // Free
arr = NULL;     // Safe
```

**Common bugs:**
- Not checking NULL
- Forgetting to free (leak)
- Double free
- Use after free
- Freeing non-malloced memory

---

### ✅ Lesson 33: calloc and realloc

**calloc - Allocate and zero:**
```c
void *calloc(size_t count, size_t size);

int *arr = calloc(5, sizeof(int));  // 5 zeros, not garbage!
// Result: [0, 0, 0, 0, 0]
```

**realloc - Resize memory:**
```c
void *realloc(void *ptr, size_t new_size);

int *arr = malloc(5 * sizeof(int));
arr = realloc(arr, 10 * sizeof(int));  // Grow to 10
```

**Safe realloc pattern:**
```c
int *temp = realloc(arr, new_size);
if (temp == NULL) {
    // realloc failed, arr still valid
} else {
    arr = temp;  // Only update on success
}
```

**calloc vs malloc:**
| Function | Memory After | Speed |
|----------|--------------|-------|
| `malloc` | Garbage | Fast |
| `calloc` | Zeros | Slower |

---

### ✅ Lesson 34: Dynamic Arrays

**Dynamic array pattern:**

```c
int *arr = malloc(5 * sizeof(int));  // Initial capacity
int size = 0;
int capacity = 5;

// When full, grow!
if (size == capacity) {
    capacity *= 2;  // Double
    arr = realloc(arr, capacity * sizeof(int));
}
```

**Growth strategies:**
- Incremental (+1): Too many reallocs
- Doubling (×2): Optimal - O(1) amortized

**Why doubling?**
- 1000 elements = ~10 reallocs (not 1000!)
- Less frequent copying = faster

---

## Chapter 10: Dynamic Memory - Summary

**Key Takeaways:**
- Stack = automatic, limited; Heap = manual, large
- `malloc` allocates raw (garbage) memory
- `calloc` allocates zeroed memory
- `realloc` resizes existing memory
- Always `free()` what you `malloc()`
- Dynamic arrays grow by doubling capacity

**Functions:**
| Function | Purpose |
|----------|---------|
| `malloc(size)` | Allocate raw memory |
| `calloc(n, size)` | Allocate + zero |
| `realloc(ptr, size)` | Resize |
| `free(ptr)` | Release |

**Best practices:**
- Check malloc for NULL
- Free all allocations
- Set pointer to NULL after free
- Use temp variable with realloc

---

## Quick Reference - Complete C Summary

**Data Types:**
| Type | Use When |
|------|----------|
| `char` | Characters, small numbers |
| `int` | Default for integers |
| `float` | Decimals (memory matters) |
| `double` | Decimals (precision matters) |
| `struct` | Group related data |
| `void*` | Generic pointer |

**Control Flow:**
| Keyword | Purpose |
|----------|---------|
| `if/else` | Conditional execution |
| `for/while` | Loops |
| `break` | Exit loop/switch |
| `continue` | Skip to next iteration |

**Pointers:**
| Symbol | Meaning |
|--------|---------|
| `&` | Address of |
| `*` | Dereference |
| `->` | Struct field via pointer |
| `[]` | Array indexing |

**Memory:**
| Function | Purpose |
|----------|---------|
| `malloc` | Allocate raw |
| `calloc` | Allocate zeroed |
| `realloc` | Resize |
| `free` | Release |

**Format Specifiers:**
| Specifier | Type |
|-----------|------|
| `%d` | int |
| `%f` | double |
| `%c` | char |
| `%s` | string |
| `%p` | pointer/address |

---

*End of C Programming Notes*
