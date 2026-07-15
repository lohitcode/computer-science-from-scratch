# C & Data Structures Learning System

## 🤖 AI Instructions (READ THIS FIRST)

When user says **"start"** or **"continue"**:

1. Read `PROGRESS.md` → Check what's completed
2. Read `main.c` → See what function they're on
3. Read `README.md` → Check current lesson
4. Tell them: **Where they are**, **What to do**, **Ask if they need help**

When user says **"done"**:

1. Save `main.c` → `completed/[topic]-part[X].c`
2. Update `PROGRESS.md` with ✅
3. Add ONE new function to `main.c`
4. Update `test.c` and `README.md`
5. Tell them what's next

**ALWAYS:** One function at a time. Never more.

---

## Overview

Interactive C learning environment for deep systems intuition. Learn by implementing one function at a time, with immediate test feedback.

---

## File Structure

```
/Users/lohit/Desktop/c/
├── main.c           # ← ONLY file user edits (one function at a time)
├── test.c           # ← Tests for current step (I write this)
├── Makefile         # ← Build system (user runs: make test)
├── README.md        # ← Current lesson (history, mental model, guide)
├── PROGRESS.md      # ← Progress checklist
├── AGENTS.md        # ← Codex repository instructions
└── completed/       # ← Archive of passed code
    ├── arrays.c
    ├── linked-lists.c
    └── ...
```

---

## Core Principles

### 1. ONE PROBLEM AT A TIME (CRITICAL)

**🔴 THIS IS THE MOST IMPORTANT RULE**

**main.c MUST have only:**
- **ONE** placeholder function to implement (like LeetCode)
- OR **TWO** only if they're tightly coupled (e.g., create/destroy)
- NEVER more than 2 functions at once

**If a topic has 5 functions:**
```
❌ WRONG: Put all 5 in main.c at once
✅ RIGHT:  Split into 5 separate parts
```

**Example progression (Arrays):**
```
Part 1: main.c has create() + destroy()
        → User implements
        → Tests pass
        → User says "done"

Part 2: main.c has get() + size()
        → User implements
        → Tests pass
        → User says "done"

Part 3: main.c has append()
        → User implements
        → Tests pass
        → User says "done"
```

**Why?**
- LeetCode-style focus: one problem, one solution
- Less overwhelming
- Faster feedback loop
- Builds confidence incrementally
- User can say "skip" to move past just ONE thing

**For AI:**
- Always split tasks into smallest possible units
- If a data structure needs 7 functions, make 7 parts
- Update main.c to ONLY show the current function(s)
- Keep previous functions implemented (don't remove them)
- Add NEW functions one at a time

### 2. Immediate Feedback Loop
```
Edit main.c → make test → See results → Iterate → Pass → Next function
```

### 3. Deep Understanding First
- Historical context (why/when invented)
- Memory visualization (ASCII diagrams)
- Trade-offs vs alternatives
- Only then: implementation

### 4. Test-Driven Validation
- User runs `make test` themselves
- Clear pass/fail output with colors
- Only proceed when ALL tests pass

---

## 🔄 How to Resume (When User Says "start" or "continue")

**CRITICAL: AI must follow this workflow when user says "start" or "continue"**

```
User: "start" or "continue"
```

**AI Action Steps:**

1. **Read PROGRESS.md** → See what's completed, what's current
2. **Read main.c** → See what function user is working on
3. **Read README.md** → See what lesson they're on
4. **Determine state:**
   - Are they stuck on current function? → Help them
   - Did they just say "done"? → Move to next function
   - Is this a fresh session? → Show context

5. **Respond with:**
   - Where they left off (topic, part, function)
   - Quick recap of current task
   - Ask: "Want me to explain the concept or help debug?"

**Example response:**
```
Welcome back! You're on:

→ Arrays - Part 1: Create & Destroy
→ Current function: int_array_create()

You're implementing malloc for the IntArray struct.
Run 'make test' to check your progress.

Need help with the concept or stuck on something?
```

**Why?**
- User can switch terminals/devices
- AI maintains context across sessions
- Clear resumption point
- No "where was I?" confusion

## Workflow

### Per Topic (e.g., Arrays)

**Phase 1: Foundation** (create, destroy)
- User implements basic allocation/deallocation
- Tests verify memory is set up correctly

**Phase 2: Access** (get, size)
- User implements read operations
- Tests verify element access works

**Phase 3: Modify** (append, insert, remove)
- User implements write operations
- Tests verify data manipulation

**Phase 4: Advanced** (resize, etc.)
- User implements complex behaviors
- Tests verify edge cases

### Per Function

1. **I update main.c** - Add new function(s) with TODO comments
2. **I update test.c** - Add tests for new function(s)
3. **I update README.md** - Explain the concept for this step
4. **User implements** - Writes the code
5. **User runs `make test`** - Sees results
6. **User iterates** - Until all pass
7. **User says "done"** - I save and advance

---

## Lesson Format (README.md)

Each lesson step includes:

```markdown
# Topic - Part X

## 📚 History/Context
- When and why this was invented
- What problem it solved
- What came before it

## 🧠 Mental Model
- ASCII memory diagrams
- Visual explanations
- Trade-offs

## ⚡ Your Task
- Function(s) to implement
- Step-by-step guide
- Code examples

## 🎯 Test Criteria
- What make test should show
- Expected output

## 🚀 Quick Reference
- Relevant C functions/keywords
```

---

## Test Format (test.c)

```c
// Color output for clarity
#define COLOR_GREEN "\033[0;32m"
#define COLOR_RED "\033[0;31m"
// ...

// Test framework
void test_start(const char *name);
void test_assert(int condition, const char *test_name);
void test_summary();

// Test functions
void test_[feature]();

// Main runner calls all tests
int main() {
    test_[feature1]();
    test_[feature2]();
    // ...
    test_summary();
}
```

---

## Progress Tracking (PROGRESS.md)

```markdown
## C Foundations
- [ ] Pointers & Memory
- [ ] Structs
- ...

## Data Structures
- [ ] Arrays ← Current
- [ ] Linked Lists
- ...

## Completed Archives
- arrays.c (completed on 2026-05-26)
```

---

## Curriculum Order

### C Foundations (Quick Refresh)
1. Pointers & Memory Visualization
2. Structs & Memory Layout
3. Function Pointers
4. malloc, free, calloc, realloc

### Data Structures (Historical Evolution)
1. **Arrays** - Contiguous memory, O(1) access
2. **Linked Lists** - Solving array resize, cache trade-off
3. **Stacks** - LIFO, call stacks, expression parsing
4. **Queues** - FIFO, scheduling, buffering
5. **Hash Tables** - O(1) lookup, collision handling
6. **Binary Trees** - Hierarchical data, traversal
7. **Binary Search Trees** - Ordered data, logarithmic ops
8. **Heaps** - Priority queues, array representation
9. **Graphs** - Networks, adjacency, BFS/DFS
10. **Tries** - Prefix matching, autocomplete
11. **AVL Trees** - Self-balancing basics

---

## When User Says "Done"

1. **ONLY add ONE new function** to main.c (or 2 if coupled)
2. Keep previous functions (don't remove them)
3. Update test.c with tests for the NEW function only
4. Update README.md with lesson for the NEW function
5. Save full `main.c` → `completed/[topic]-part[X].c` (optional archive)
6. Update `PROGRESS.md` with progress

**Remember:** ONE problem at a time. Always split if needed.

---

## Makefile Commands

```makefile
make test    # Compile and run tests
make clean   # Remove build artifacts
make all     # Just compile
```

---

## User Commands

- **"start" / "continue"** → Resume from where we left off (reads PROGRESS.md)
- **"done" / "passed"** → Tests all passing, move to next function
- **"help"** → Show current context and what to work on
- **"skip"** → Skip current step (not recommended, but available)
- **"explain [X]"** → Re-explain a concept

---

## Code Quality

- **Wall flags**: `-Wall -Wextra` in Makefile
- **Standard**: `-std=c11`
- **Debug**: `-g` for potential debugging
- **Comments**: Use sparingly, only for non-obvious WHY

---

## main.c Template Structure

```c
// =====================================================
// TOPIC - Part X
// =====================================================
// Your task: Implement [function name]
// Run: make test
// =====================================================

#include <stdlib.h>
#include <stdio.h>

typedef struct {
    // ... fields ...
} SomeStruct;

// Previous functions (already implemented, keep them)
SomeStruct* some_struct_create(int capacity) {
    // ... user's working code ...
}

void some_struct_destroy(SomeStruct *s) {
    // ... user's working code ...
}

// =====================================================
// TODO: Implement THIS function (ONLY ONE NEW ONE)
// =====================================================

int some_struct_get(SomeStruct *s, int index) {
    // TODO: Implement this
    return 0;  // Replace this
}
```

**Key points:**
- Previous functions stay (don't delete working code)
- Only ONE new TODO function added
- Clear comments showing what to focus on

---

## Example Progression (Arrays)

| Part | main.c Contains | User Focuses On | Tests |
|------|-----------------|-----------------|-------|
| 1 | `create()`, `destroy()` | malloc, free, two allocations | create & destroy |
| 2 | `create()`, `destroy()`, `get()`, `size()` | Pointer access, struct fields | get & size |
| 3 | `...` + `append()` | Resize logic, reallocation | append |
| 4 | `...` + `insert()` | Shifting elements right | insert |
| 5 | `...` + `remove()` | Shifting elements left | remove |
| 6 | All functions + edge cases | Bounds, null handling | full suite |

**Key:** Each part = separate main.c update, separate test run, separate "done" from user.

---

## Memory Visualization Style

Use ASCII diagrams for everything:

```
Stack:        Heap:
arr ──┐      ┌──→ [IntArray struct]
       │      │    • data ───┐
       └──────┘              │
                             ▼
                        [ 10 | 20 | 30 | ? | ? ]
```

Show:
- Pointers with arrows
- Memory addresses
- Both stack and heap
- Before/after states

---

## Testing Philosophy

- **Test first, code second** - Tests define the contract
- **Small tests** - One assertion per logical check
- **Clear names** - `test_create_basic` not `test_1`
- **Null safety** - Always test NULL inputs
- **Edge cases** - Empty, single element, at capacity

---

## Historical Context Template

For each data structure:

1. **Era**: When invented (decade)
2. **Problem**: What was broken before
3. **Solution**: What this DS introduced
4. **Trade-offs**: What we gained/lost
5. **Evolution**: What came after

---

## Future Topics (Post-Arrays)

- **Linked Lists**: Why linked? When to use? Cache implications
- **Stacks**: Call stack, undo systems, balanced parentheses
- **Queues**: Producer-consumer, task scheduling
- **Hash Tables**: Hash functions, collisions, chaining vs probing
- **Trees**: Hierarchies, DOM, file systems
- **BST**: Ordered data, why not hash?
- **Heaps**: Priority queues, why array representation?
- **Graphs**: Social networks, dependencies, pathfinding
