# Go Learning - From C to Go

**Progress:** Learning from scratch, comparing with C

---

## ✅ COMPLETED TOPICS

---

## TOPIC 1: Package System & Entry Point

### Why packages?

**C approach:**
- Files are just files
- `#include` to share code
- No namespacing

**Go approach:**
- Every file belongs to a **package**
- Packages organize code
- `import` instead of `#include`

### Package main vs others

```c
/* C - main.c */
#include <stdio.h>

int main() {
    printf("Hello\n");
    return 0;  // Required
}
```

```go
// Go - main.go
package main  // ← Required for executables!

import "fmt"  // ← Import, not include

func main() {  // ← func, not int main()
    fmt.Println("Hello")
    // No return 0 needed - automatic
}
```

**Key differences:**
1. `package main` tells Go "this is an executable program"
2. Other packages (like `fmt`) are **libraries**, not executables
3. `func main()` returns nothing (unlike C's `int main()`)

### Why this design?

| Problem in C | Go Solution |
|--------------|-------------|
| No namespacing | Packages provide isolation |
| Header file complexity | Import hides details |
| Linker issues | Go handles linking automatically |

---

## TOPIC 2: Import System

### C #include vs Go import

```c
/* C */
#include <stdio.h>    // Standard library
#include "myheader.h" // Your own header
```

```go
// Go
import "fmt"     // Standard library
import "mymath"   // Your own package (no quotes needed)
```

**Key difference:**
- C: Two forms (`<>` vs `""`) mean different search paths
- Go: One form, Go figures out where packages are

### Multiple imports

```c
/* C */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
```

```go
// Go - Method 1: Multiple lines
import "fmt"
import "os"
import "strings"

// Go - Method 2: Factored import (preferred!)
import (
    "fmt"
    "os"
    "strings"
)
```

### Unused imports

```c
/* C */
#include <stdio.h>  // Can include unused headers
                     // No error (just slower compile)
```

```go
// Go
import "fmt"  // If you don't use fmt
               // Go won't compile! ERROR!
```

**Why?** Go forces clean code - no unused imports allowed.

---

## TOPIC 3: Printing Functions

### C printf vs Go fmt

```c
/* C */
printf("Hello\n");           // No newline
printf("Age: %d\n", 25);    // Format string
puts("Hello");               // Adds newline
```

```go
// Go
fmt.Print("Hello")           // No newline
fmt.Println("Hello")        // Adds newline automatically!
fmt.Printf("Age: %d\n", 25)  // Format printing
```

**Comparison:**

| C | Go | Notes |
|---|-----|-------|
| `printf("...\n")` | `fmt.Println("...")` | Go adds `\n` for you |
| `printf("Age: %d", x)` | `fmt.Printf("Age: %d", x)` | Same format! |
| `puts("...")` | `fmt.Println("...")` | Both add newline |

### Format verbs (same as C!)

```c
/* C */
printf("%d %f %s", 42, 3.14, "hello");
```

```go
// Go - SAME VERBS!
fmt.Printf("%d %f %s", 42, 3.14, "hello")
```

| Verb | C | Go | Meaning |
|------|---|-----|---------|
| `%d` | ✓ | ✓ | Integer |
| `%f` | ✓ | ✓ | Float |
| `%s` | ✓ | ✓ | String |
| `%p` | ✓ | ✓ | Pointer |
| `%c` | ✓ | ✓ | Character |
| `%v` | ✗ | ✓ | **NEW!** Any value (default format) |
| `%#v` | ✗ | ✓ | **NEW!** Go syntax format |

### New Go verbs:

```go
name := "Lohit"
age := 25

// %v - default format for any type
fmt.Printf("%v, %v", name, age)  // Lohit, 25

// %#v - Go syntax format
fmt.Printf("%#v", name)  // "Lohit"
```

---

## RUNNING CODE

### C vs Go

```bash
# C
gcc main.c -o main  # Compile
./main              # Run

# Go - Option 1 (like python)
go run main.go      # Compile + run in one command

# Go - Option 2 (build binary)
go build main.go    # Creates executable
./main              # Run it

# Go - Format your code
go fmt main.go      # Auto-format (like prettier)
```

---

## SUMMARY: Topic 1-3

| Concept | C | Go |
|---------|---|-----|
| Entry point | `int main()` | `func main()` in `package main` |
| Include/import | `#include <stdio.h>` | `import "fmt"` |
| No newline print | `printf("text")` | `fmt.Print("text")` |
| Newline print | `printf("text\n")` | `fmt.Println("text")` |
| Format print | `printf("%d", x)` | `fmt.Printf("%d", x)` |
| Return value | `return 0;` needed | Automatic (optional) |

---

**PROGRESS:** ✅ Package system, imports, printing completed

---

## ⏳ NEXT TOPICS

- [ ] Variables & Types
- [ ] Control Flow
- [ ] Functions
- [ ] Arrays & Slices
- [ ] Maps
- [ ] Structs
- [ ] Pointers
- [ ] Methods & Interfaces
