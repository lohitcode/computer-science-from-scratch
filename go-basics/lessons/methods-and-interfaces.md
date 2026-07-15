# Go: Methods & Interfaces - Interactive Lesson

**Learning from scratch, step by step**

---

## Part 1: Functions vs Methods

### Function (what you know)
```go
func Area(c Circle) float64 {
    return math.Pi * c.Radius * c.Radius
}

// Usage: Area(circle)
```

### Method (new concept)
```go
func (c Circle) Area() float64 {
    return math.Pi * c.Radius * c.Radius
}

// Usage: circle.Area()
```

**The difference:** `(c Circle)` is called the "receiver" - it's like `this` in JavaScript or `self` in Python!

---

## Part 2: Value vs Pointer Receivers

### Value receiver (gets a copy)
```go
func (c Circle) Area() float64 {
    // Can read c.Radius, but changing it won't affect original
    return math.Pi * c.Radius * c.Radius
}
```

### Pointer receiver (can modify!)
```go
func (c *Circle) Scale(factor float64) {
    c.Radius *= factor  // This DOES modify the original!
}
```

**Rule of thumb:** Use pointer receiver if you need to modify.

---

## Part 3: What is an Interface?

An interface is a list of methods. If a type has those methods, it satisfies the interface!

```go
// Interface definition (just method signatures)
type Shape interface {
    Area() float64
    Perimeter() float64
}
```

**Key:** Go **automatically** detects if a type satisfies an interface. No `implements` keyword needed!

```go
// If Circle has Area() and Perimeter()...
// It IS a Shape! No extra code needed.
```

---

## Part 4: Why Interfaces? (Polymorphism)

```go
func Describe(s Shape) {
    fmt.Printf("Area: %f\n", s.Area())
}

// Can pass ANYTHING that satisfies Shape:
var circle Shape = Circle{Radius: 5}
var rect Shape = Rectangle{Width: 10, Height: 20}

Describe(circle)  // Works!
Describe(rect)     // Works!
```

**Same function, different types!** That's polymorphism.

---

## ✅ Summary

| Concept | Syntax | Usage |
|---------|--------|-------|
| Method | `func (c Circle) Area()` | `circle.Area()` |
| Pointer method | `func (c *Circle) Scale()` | `circle.Scale()` |
| Interface | `type Shape interface { ... }` | As variable type |
| Satisfying | Implement methods | Automatic! |

---

Now let's practice with smaller problems!
