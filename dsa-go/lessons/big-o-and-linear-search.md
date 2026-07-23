# Big O and Linear Search

## Begin with the problem, not the terminology

Imagine a written list of names. Someone asks whether “Lohit” is present.

If the names have no special order and you know nothing else about the list,
the only reliable strategy is to inspect them one at a time:

```text
Anita -> Dev -> Isha -> Lohit
 no      no      no      yes
```

That simple act already contains the foundations of DSA:

- **data**: the names;
- **data structure**: the ordered list holding them;
- **algorithm**: the repeatable procedure used to search;
- **correctness**: the procedure finds the name if it is present;
- **cost**: the number of names that must be inspected.

Data structures organize information. Algorithms are precise, finite
procedures for transforming information or answering questions about it.

The two are inseparable. How data is arranged determines which operations are
cheap, and the operations we need influence how we arrange the data.

## A short history: algorithms are older than computers

Algorithms did not begin with electronic machines.

- Ancient arithmetic methods gave people repeatable procedures for
  calculation. Euclid described an algorithm for finding the greatest common
  divisor more than two thousand years ago.
- Around the ninth century, the Persian scholar Muhammad ibn Musa
  al-Khwarizmi wrote influential works describing systematic calculation. The
  word *algorithm* ultimately developed from the Latin form of his name.
- Mechanical calculators, punched-card machines, and later electronic
  computers made it possible to execute increasingly long procedures
  automatically.
- In the late nineteenth century, mathematicians developed asymptotic notation
  for describing how functions grow. Computer scientists later adopted this
  language because counting exact seconds tied an algorithm to one machine.
- As programs and datasets grew, it became clear that choosing a representation
  and an algorithm could matter more than buying a faster computer.

This history gives us an important mental model:

> A computer does not understand the goal. It performs the exact sequence of
> steps we specify.

An algorithm therefore needs:

1. clearly defined input;
2. clearly defined output;
3. unambiguous steps;
4. a point at which it terminates;
5. a reason we believe its result is correct.

## Why study DSA in Go?

Go gives us useful high-level tools such as slices and maps, while still making
important details visible:

- indexes expose the sequential layout of a slice;
- pointers help us construct linked structures and trees;
- explicit loops make the work performed by an algorithm easy to see;
- goroutines and channels will later let us distinguish an algorithm from the
  way its work is scheduled concurrently.

For now, we will use a slice and an ordinary loop. There is no library call
hiding the search from us.

## First principles: what can the machine actually do?

At this level, a machine can perform small operations:

```text
read a value
compare two values
change a variable
jump to another instruction
return a result
```

Linear search is built from exactly those operations:

```text
read one element -> compare it -> either return or continue
```

We need a way to discuss how many such operations may be required when the
input becomes larger. That is where complexity analysis begins.

## Measuring cost

We could time a program, but elapsed time changes with:

- the CPU;
- other programs currently running;
- the Go compiler and version;
- the exact input;
- caching and memory behavior.

Timing is valuable when benchmarking a real implementation. It is not a stable
mathematical description of the underlying algorithm.

Instead, we first count how the work grows with the input.

Before comparing algorithms, we need a way to describe how their resource usage changes as the input grows. Big-O notation gives us that vocabulary.

## Input size

We usually write the input size as `n`.

For a slice:

```go
numbers := []int{4, 2, 9, 7, 5}
```

the input size is:

```text
n = len(numbers) = 5
```

If the slice contained one million numbers, then `n` would be one million.

Big O does not primarily ask how many nanoseconds one particular computer takes. It asks:

> How does the amount of work grow when `n` grows?

## Constant time: O(1)

Accessing one known slice index takes a constant amount of work:

```go
value := numbers[3]
```

Whether the slice contains 5 elements or 5 million elements, retrieving index `3` is still one direct access.

```text
input size:     5       100       1,000,000
index accesses: 1         1               1
```

This is `O(1)`.

`O(1)` does not mean the operation takes exactly one CPU instruction. It means the work does not grow with `n`.

## Linear time: O(n)

Suppose we do not know where a value is located. We can examine each element from left to right:

```text
[4, 2, 9, 7, 5]
 ^  ^  ^  ^
 check until 7 is found
```

In the worst case, the target is:

- at the final index; or
- absent from the slice.

Then every element must be checked:

```text
input size:  5       100       1,000,000
max checks:  5       100       1,000,000
```

The work grows in direct proportion to the input size, so linear search is `O(n)`.

## Big O describes growth

Imagine two algorithms:

```text
Algorithm A performs n operations.
Algorithm B performs 3n + 10 operations.
```

Both are `O(n)` because both grow linearly. Big O normally ignores constant multipliers and fixed additions:

```text
O(3n + 10) -> O(n)
```

This abstraction lets us compare growth patterns without depending on a particular CPU, compiler, or small implementation detail.

## Common growth rates

From generally better-scaling to worse-scaling:

| Big O | Name | Example |
|---|---|---|
| `O(1)` | Constant | Accessing a known slice index |
| `O(log n)` | Logarithmic | Binary search in sorted data |
| `O(n)` | Linear | Scanning every element |
| `O(n log n)` | Linearithmic | Efficient comparison sorting |
| `O(n²)` | Quadratic | Comparing every pair |
| `O(2ⁿ)` | Exponential | Exploring every subset choice |

The actual fastest algorithm for tiny inputs can depend on constants, but growth rate becomes increasingly important as inputs become large.

## Best, worst, and average cases

For linear search:

```text
target at index 0     -> 1 check       -> best case
target near middle   -> about n/2      -> average intuition
target absent        -> n checks       -> worst case
```

The best case is `O(1)`, but linear search is normally described as `O(n)` because its worst-case work grows linearly.

When someone states an algorithm's Big O without qualification, they usually mean its upper-bound or worst-case growth.

## Linear search contract

Implement:

```go
func linearSearch(numbers []int, target int) int
```

It must return:

- the index of the first matching value;
- `-1` if the value does not exist.

This is the boundary between the caller and the algorithm. The caller does not
need to know how the function searches; it only relies on this promised
behavior.

Examples:

```text
linearSearch([4, 2, 9, 7, 5], 7)  -> 3
linearSearch([4, 2, 9, 7, 5], 10) -> -1
linearSearch([7, 2, 7], 7)        -> 0
linearSearch([], 7)               -> -1
```

## Why return `-1`?

Valid slice indexes begin at zero:

```text
index:  0  1  2
value: [4, 2, 9]
```

Therefore, `-1` cannot be confused with a valid index. It acts as a sentinel value meaning “not found.”

Later, you will see APIs that return `(value, bool)` or `(value, error)` instead. For this classic search function, `-1` keeps the contract simple.

## The loop mental model

Your algorithm should follow this control flow:

```text
start at index 0
      |
      v
does numbers[index] equal target?
      |
      +-- yes -> return index immediately
      |
      +-- no  -> move to next index
                       |
                       v
              any elements remaining?
                       |
                       +-- yes -> check next
                       |
                       +-- no  -> return -1
```

Returning immediately when a match is found ensures the first matching index is returned and avoids unnecessary checks.

## Why the algorithm is correct

Before each comparison, every earlier element has already been checked and is
known not to match the target. This fact is called a **loop invariant**.

If the current element matches, returning its index is correct because:

- it contains the target; and
- no earlier element contained the target.

If the loop ends, every valid element has been checked. Returning `-1` is then
correct because no match exists.

You do not need to write a formal proof in the program. Learning to state this
reasoning will help you design and debug more complicated algorithms later.

## Time complexity

Worst-case time complexity:

```text
O(n)
```

At most, the function examines every element once.

## Space complexity

The algorithm should use only a small fixed number of variables, regardless of input size:

```text
O(1) additional space
```

It does not create another slice proportional to `n`.

The input slice itself is not counted as additional space because the caller already owns it.

## Your task

Complete `dsa-go/main.go`:

1. Find the marked solution area.
2. Replace the placeholder body of `linearSearch`.
3. Scan the slice from left to right.
4. Return immediately when the target matches.
5. Return `-1` after the loop when no match exists.

Do not sort the input or create a map. Those operations would change the problem and introduce additional costs.

Do not edit `testCase`, `main`, or the provided test data. Like a coding
platform, the surrounding program owns the input and verifies your returned
answer.

## Expected output after a correct solution

```text
PASS 1: target in the middle
PASS 2: target is missing
PASS 3: first duplicate is returned
PASS 4: empty slice
PASS 5: single matching element
PASS 6: single non-matching element
PASS 7: negative target

7/7 tests passed
```

## Edge cases to think through

Before running the code, predict these results:

| Input | Target | Expected |
|---|---:|---:|
| `[]` | 7 | -1 |
| `[7]` | 7 | 0 |
| `[4]` | 7 | -1 |
| `[7, 2, 7]` | 7 | 0 |
| `[0, -2, 5]` | -2 | 1 |

You do not need separate special-case branches for empty or one-element slices. A correct loop naturally handles them.

## Common mistakes

### Returning `-1` inside the loop

If the first element does not match and you immediately return `-1`, later elements are never checked.

The “not found” return belongs after the loop.

### Returning the value instead of the index

The contract asks for the location:

```text
target value = 7
target index = 3
```

Return `3`, not `7`.

### Continuing after finding a match

If duplicates exist, continuing can return the last match instead of the first. Return immediately.

### Accessing an invalid index

Use a loop that only visits indexes from `0` through `len(numbers)-1`.

## Verification

Run from `dsa-go`:

```bash
go fmt ./...
go vet ./...
go run .
```

## Completion checklist

- [ ] `linearSearch` has the required signature
- [ ] Elements are checked from left to right
- [ ] The first matching index is returned
- [ ] Missing targets return `-1`
- [ ] Empty slices work without special handling
- [ ] No sorting or map is used
- [ ] Worst-case time complexity is understood as `O(n)`
- [ ] Additional space complexity is understood as `O(1)`
- [ ] All provided test cases pass
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go run .` succeeds

When every item passes, DSA Problem 1 is complete.
