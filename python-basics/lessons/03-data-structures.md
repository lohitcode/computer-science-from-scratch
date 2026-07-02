# Lesson 3: Data Structures

## 🔵 Lists (like Arrays)

```python
# Create
fruits = ["apple", "banana", "cherry"]

# Access
fruits[0]        # "apple"
fruits[-1]       # "cherry" (last item!)

# Slicing (unique to Python!)
fruits[0:2]      # ["apple", "banana"]
fruits[-2:]      # ["banana", "cherry"]

# Methods
fruits.append("date")    # Add to end
fruits.pop()            # Remove from end
fruits.insert(1, "x")   # Insert at index
len(fruits)             # Length
```

## 🔵 Dictionaries (like Objects)

```python
# Create (keys MUST be strings in this form)
user = {
    "name": "John",
    "age": 30,
    "email": "john@example.com"
}

# Access
user["name"]              # "John"
user.get("name")         # "John" (safer)
user.get("phone", "N/A")  # "N/A" (default if not found)

# Add/Update
user["city"] = "Bangalore"
user["age"] = 31

# Loop
for key, value in user.items():
    print(f"{key}: {value}")
```

## 🔵 Sets (unique values only)

```python
# Create
numbers = [1, 2, 2, 3, 3, 3]
unique = set(numbers)    # {1, 2, 3}

# Methods
my_set.add(4)
my_set.remove(2)
```

## 🔵 Tuples (immutable lists)

```python
# Create (can't change!)
coords = (10, 20)

# Unpacking
x, y = coords
```

## Completed Problems

- ✅ Problem 9: List operations
