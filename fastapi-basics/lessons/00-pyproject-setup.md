# Lesson: pyproject.toml Setup

## 🎯 What is `pyproject.toml`?

**This is a Python project configuration file.** It's the modern standard for Python projects (replaces `setup.py`, `requirements.txt`, etc.)

---

## 🔍 Your File Explained

```toml
[tool.pyright]
pythonPath = ".venv/bin/python3"

[tool.basedpyright]
pythonPath = ".venv/bin/python3"
```

---

## 📦 What Each Section Does

### `[tool.pyright]`

**Configuration for Pyright** (Microsoft's Python type checker)

- **Tells Pyright:** "Use `.venv/bin/python3` for this project"
- **Why:** So Pyright knows where to find installed packages (FastAPI, etc.)

### `[tool.basedpyright]`

**Configuration for basedpyright** (Zed's default Python LSP)

- **Tells basedpyright:** "Use `.venv/bin/python3` for this project"
- **Why:** Same reason - helps the LSP find your packages

---

## 📊 Comparison to Node.js

**Similar to `package.json`:**

| Node.js | Python |
|---------|--------|
| `package.json` | `pyproject.toml` |
| `engines/node` | `[tool.pyright].pythonPath` |
| `package-lock.json` | `requirements.txt` / lock files |

---

## 🎯 Why Both Sections?

**Two type checkers, two configs:**

| Tool | Config Section | Used By |
|------|---------------|---------|
| **Pyright** | `[tool.pyright]` | VS Code, some editors |
| **basedpyright** | `[tool.basedpyright]` | Zed (default) |

**Your file covers both!** Zed uses basedpyright, but if you open this project in VS Code, Pyright will also know where your venv is.

---

## 💡 Why This File Exists

**Before:** Zed couldn't find FastAPI (LSP errors)

**After:** Zed reads `pyproject.toml`, sees `pythonPath = ".venv/bin/python3"`, and now knows where to find FastAPI!

---

## 📋 Common `pyproject.toml` Sections

```toml
[tool.pyright]          # Pyright config
pythonPath = ".venv/bin/python3"

[tool.basedpyright]     # basedpyright config
pythonPath = ".venv/bin/python3"

[tool.ruff]             # Ruff formatter/linter config
lineLength = 100

[tool.pytest]           # pytest config
testpaths = ["tests"]

[project]               # Project metadata
name = "my-project"
version = "0.1.0"
dependencies = [
    "fastapi",
    "uvicorn"
]
```

---

## ✅ Summary

**Your `pyproject.toml` tells Zed:**

> "Hey, for this project, use the Python interpreter in `.venv/bin/python3`"

**That's how Zed's LSP finds FastAPI and resolves imports!** 🎯
