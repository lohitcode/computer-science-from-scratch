# Lesson 6: Decorators - The `@` Syntax

## 🎯 What Are Decorators?

**Decorator = A function that modifies another function**

Think of it as **middleware for functions** - just like Express middleware, but for individual functions.

---

## 🔵 Why Do We Need Decorators?

**Problem:** You want to add behavior to functions without changing their code.

**Example:** You want to log every function call, time how long functions take, or check if user is authenticated.

**Without decorators:** You'd have to add this code to EVERY function.

**With decorators:** Add it once, apply to any function with `@`.

---

## 📊 Real-World Example: Logging

**Without decorator (repetitive):**
```python
def get_user(user_id):
    print("Calling get_user")  # ← Added logging
    user = db.find(user_id)
    print("get_user done")      # ← Added logging
    return user

def get_post(post_id):
    print("Calling get_post")   # ← Added logging AGAIN
    post = db.find(post_id)
    print("get_post done")       # ← Added logging AGAIN
    return post
```

**With decorator (clean):**
```python
@log_calls  # ← Add this, and logging happens automatically!
def get_user(user_id):
    return db.find(user_id)

@log_calls  # ← Reuse the same decorator!
def get_post(post_id):
    return db.find(post_id)
```

---

## 🔍 How Decorators Work: Step by Step

### Step 1: Functions Are First-Class

**In Python, functions are values:**

```python
def greet(name):
    return f"Hello {name}"

# Functions can be assigned to variables
my_func = greet
print(my_func("World"))  # "Hello World"

# Functions can be passed to other functions
def run_twice(func):
    func()
    func()

def say_hi():
    print("Hi!")

run_twice(say_hi)  # Prints "Hi!" twice
```

---

### Step 2: Functions Can Return Functions

```python
def create_multiplier(factor):
    # Returns a NEW function
    def multiply(x):
        return x * factor
    return multiply

times_3 = create_multiplier(3)
print(times_3(5))  # 15

times_10 = create_multiplier(10)
print(times_10(5))  # 50
```

---

### Step 3: A Decorator Is Just A Function

```python
def my_decorator(func):
    # func is the function being decorated
    def wrapper():
        print("Before!")
        result = func()
        print("After!")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Before!
# Hello!
# After!
```

---

## 🔷 What The `@` Actually Does

**This:**
```python
@my_decorator
def say_hello():
    print("Hello!")
```

**Is the same as:**
```python
def say_hello():
    print("Hello!")

say_hello = my_decorator(say_hello)
#           ↑
#    Replaces say_hello with the wrapper
```

**`@` is just syntactic sugar!** It makes the code cleaner.

---

## 📦 Creating Your Own Decorators

### Example 1: Timing Function

```python
import time

def time_it(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@time_it
def slow_function():
    time.sleep(1)
    return "Done"

slow_function()  # "slow_function took 1.00s"
```

---

### Example 2: Authentication Check

```python
def require_auth(func):
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            raise Exception("Not authenticated!")
        return func(*args, **kwargs)
    return wrapper

@require_auth
def delete_user(user_id):
    # This only runs if user is authenticated
    return db.delete(user_id)
```

---

### Example 3: Memoization (Caching)

```python
def memoize(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# First call: slow
fibonacci(100)  # Takes time

# Second call: instant (cached!)
fibonacci(100)  # Instant!
```

---

## 🎯 Decorators with Arguments

**Sometimes you want decorators that take parameters:**

```python
def repeat(times):
    # This returns the actual decorator
    def decorator(func):
        def wrapper():
            for _ in range(times):
                func()
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")

say_hello()
# Output:
# Hello!
# Hello!
# Hello!
```

---

## 🔷 Preserving Function Metadata

**Problem:** Decorators replace your function with `wrapper`, losing metadata.

```python
@time_it
def important_function():
    """This is important!"""
    pass

print(important_function.__name__)  # "wrapper" (wrong!)
print(important_function.__doc__)   # None (wrong!)
```

**Solution:** Use `@functools.wraps`

```python
from functools import wraps

def time_it(func):
    @wraps(func)  # ← Preserves metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@time_it
def important_function():
    """This is important!"""
    pass

print(important_function.__name__)  # "important_function" (correct!)
print(important_function.__doc__)   # "This is important!" (correct!)
```

---

## 📊 Comparison: JavaScript vs Python

### JavaScript Middlewares

```javascript
// Express middleware
app.use((req, res, next) => {
    console.log("Request:", req.url);
    next();
});

app.get("/", (req, res) => {
    res.json({ message: "Hello" });
});
```

### Python Decorators

```python
# Function decorator
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} done")
        return result
    return wrapper

@log_calls
def get_home():
    return {"message": "Hello"}
```

**Key difference:**
- **JavaScript:** Middleware applies to ALL routes
- **Python:** Decorators apply to specific functions

---

## 🚀 How FastAPI Uses Decorators

### Route Decorators

```python
@app.get("/")        # Registers this function for GET /
async def root():    # When GET / is called, run this
    return {"message": "Hello"}

@app.post("/users")  # Registers this function for POST /users
async def create_user():  # When POST /users is called, run this
    return {"created": True}
```

**What FastAPI does:**
```python
class FastAPI:
    def get(self, path):
        # Returns a decorator function
        def decorator(func):
            # Stores: "When someone calls GET {path}, run func"
            self.routes[path] = {"GET": func}
            return func
        return decorator

# So @app.get("/") becomes:
# 1. Call app.get("/") → returns decorator
# 2. Call decorator(root) → registers root for path "/"
```

---

### Parameter Decorators

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # FastAPI reads the type hint (int)
    # Automatically converts and validates!
    return {"user_id": user_id}
```

**FastAPI uses decorators to:**
- Register routes
- Read type hints for validation
- Generate documentation
- Handle request/response parsing

---

## 📋 Common Built-in Decorators

### `@staticmethod`

```python
class Math:
    @staticmethod
    def add(x, y):
        return x + y

# No need to create instance
Math.add(1, 2)  # 3
```

### `@classmethod`

```python
class User:
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])

# Creates instance from dict
user = User.from_dict({"name": "John", "email": "john@example.com"})
```

### `@property`

```python
class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

person = Person("John", "Doe")
print(person.full_name)  # "John Doe" (like a property, not a method!)
```

---

## 🎯 When to Use Decorators

| Use Case | Example |
|----------|---------|
| **Logging** | `@log_calls` |
| **Timing** | `@time_it` |
| **Authentication** | `@require_auth` |
| **Caching** | `@memoize` |
| **Validation** | `@validate_input` |
| **Retry logic** | `@retry(max_attempts=3)` |
| **Rate limiting** | `@rate_limit(max_calls=100)` |
| **Error handling** | `@handle_errors` |

---

## ✅ Summary

| Concept | Description |
|---------|-------------|
| **Decorator** | Function that modifies another function |
| **`@` syntax** | Shorthand for applying decorator to function below |
| **How it works** | `func = decorator(func)` |
| **`*args, **kwargs`** | Passes all arguments to original function |
| **`@functools.wraps`** | Preserves function metadata |
| **FastAPI uses** | Route registration, validation, documentation |

---

## 🎯 Key Takeaways

1. **Decorators = Middleware for functions**
2. **`@decorator`** = `func = decorator(func)`
3. **Used for:** Logging, timing, auth, caching, validation
4. **`*args, **kwargs`** = Pass all arguments through
5. **`@functools.wraps`** = Preserve function metadata
6. **FastAPI decorators** = Register routes and add behavior

---

**Decorators are heavily used in FastAPI for routes, middleware, and dependency injection!**

**Next:** You'll see more decorators in FastAPI problems!
