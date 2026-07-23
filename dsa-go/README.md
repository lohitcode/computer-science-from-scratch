# Data Structures and Algorithms with Go

This track studies how software stores information, how it transforms that
information, and how to reason about the cost of doing so.

The goal is not to memorize interview solutions. The goal is to build each idea
from the problem that made it necessary, understand its trade-offs, implement
it in Go, and recognize where it appears in real software.

## How to Use This Track

For each problem:

1. Read the lesson and predict the exercise output.
2. Explain the algorithm in plain language before coding it.
3. Open `main.go` and write only inside the marked solution area.
4. Use the provided test cases to check normal and boundary behavior.
5. Run the formatter, static analyzer, and program.
6. Explain the time and additional-space complexity.
7. Commit the completed problem before starting the next one.

```bash
go fmt ./...
go vet ./...
go run .
```

## LeetCode-Style Exercise Format

Every `main.go` will already contain:

- the problem statement and constraints;
- the required function name and parameters;
- representative test cases;
- a test runner that compares actual and expected results;
- clear pass or fail output.

You should edit only the code between:

```go
// ==================== SOLUTION AREA ====================

// ================== END SOLUTION AREA ==================
```

This keeps your attention on designing the algorithm. You will not need to
rewrite the question, build the test harness, or manually print example
results. The starter may intentionally fail until your solution is complete.

## Course Map

The order is deliberate. Each section introduces a limitation that motivates
the next data structure or algorithm.

### Part I — What Is an Algorithm?

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 1 | [Big O and linear search](lessons/big-o-and-linear-search.md) | How do we find something when all we have is a sequence? | Current |
| 2 | Arrays, slices, and memory | Why is indexed access fast, and why can insertion be costly? | Planned |
| 3 | Binary search | What becomes possible when the data is sorted? | Planned |
| 4 | Recursion and the call stack | How can a problem be expressed in terms of smaller versions of itself? | Planned |

### Part II — Linear Data Structures

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 5 | Singly linked lists | What if elements must grow without occupying one continuous block? | Planned |
| 6 | Doubly linked lists | What does backward traversal cost us? | Planned |
| 7 | Stacks | How do we model “last in, first out”? | Planned |
| 8 | Queues and ring buffers | How do we process work in arrival order efficiently? | Planned |
| 9 | Hash tables | Can we find a value without scanning or sorting? | Planned |

### Part III — Sorting and Algorithmic Thinking

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 10 | Selection sort | What is the simplest way to repeatedly choose the next item? | Planned |
| 11 | Insertion sort | Why can nearly sorted data be useful? | Planned |
| 12 | Merge sort | How does divide-and-conquer improve scaling? | Planned |
| 13 | Quicksort | How can partitioning produce fast practical sorting? | Planned |
| 14 | Stability and comparison limits | What properties make one sort suitable for a particular job? | Planned |

### Part IV — Trees and Priority

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 15 | Trees and traversal | How do we represent hierarchical information? | Planned |
| 16 | Binary search trees | Can structure keep search and updates efficient? | Planned |
| 17 | Balanced-tree intuition | What goes wrong when a search tree becomes a chain? | Planned |
| 18 | Heaps and priority queues | How do we repeatedly retrieve the most important item? | Planned |
| 19 | Tries | How can shared prefixes accelerate text lookup? | Planned |

### Part V — Graphs

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 20 | Graph representations | How do we model arbitrary relationships? | Planned |
| 21 | Breadth-first search | How do we explore by distance from a starting point? | Planned |
| 22 | Depth-first search | How do we explore one path fully before backtracking? | Planned |
| 23 | Topological sorting | How do we order work with dependencies? | Planned |
| 24 | Dijkstra's algorithm | How do we find cheapest paths with non-negative costs? | Planned |

### Part VI — Problem-Solving Patterns

| # | Lesson and problem | Central question | Status |
|---:|---|---|---|
| 25 | Two pointers | When can two moving positions replace nested loops? | Planned |
| 26 | Sliding windows | How do we reuse work across neighboring ranges? | Planned |
| 27 | Backtracking | How do we explore choices and undo them safely? | Planned |
| 28 | Greedy algorithms | When is the best immediate choice globally correct? | Planned |
| 29 | Dynamic programming | How do we avoid solving the same subproblem repeatedly? | Planned |
| 30 | Capstone | How do we choose structures and algorithms for a complete system? | Planned |

## The First-Principles Lens

Every topic in this track will answer the same five questions:

1. **Problem:** What limitation are we trying to overcome?
2. **Representation:** How is the information arranged in memory?
3. **Operations:** What can we do with that representation?
4. **Cost:** How do time and additional memory grow with the input?
5. **Trade-off:** What becomes easier, and what becomes harder?

This prevents Big-O notation from becoming a collection of symbols detached
from actual programs.

## Current Problem

Start with [Lesson 1: Big O and Linear Search](lessons/big-o-and-linear-search.md),
then implement only the marked solution function in [`main.go`](main.go). The
problem statement and tests are already provided.
