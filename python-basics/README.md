# Python for JavaScript Developers

**Current: Lesson 5 - Async & Error Handling (FINAL LESSON!)**

---

## 📚 Quick Reference

For full lesson content, see: **[lessons/05-async-error-handling.md](lessons/05-async-error-handling.md)**

Previous lessons:
- **[lessons/01-variables-types.md](lessons/01-variables-types.md)**
- **[lessons/02-functions-control-flow.md](lessons/02-functions-control-flow.md)**
- **[lessons/03-data-structures.md](lessons/03-data-structures.md)**
- **[lessons/04-classes-type-hints.md](lessons/04-classes-type-hints.md)**

---

## 🔵 Context Managers (Current Problem - FINAL!)

The `with` statement automatically handles cleanup (like `finally` blocks):

```python
with open("file.txt", "r") as f:
    content = f.read()
# File closes automatically here!
```

**JavaScript equivalent (more complex):**
```javascript
const f = openFile("file.txt");
try {
    const content = f.read();
} finally {
    f.close();
}
```

**Python's `with` is cleaner!** Automatically closes resources.

---

**See `main.py` for your current exercise!**
