# Python Virtual Environments - Complete Guide

## 🤔 Why Do We Need Virtual Environments?

**Problem:** Python dependencies are global by default.

```
npm install axios        → Only in this project (node_modules/)
pip install fastapi       → GLOBALLY installed! ⚠️
```

**Why this is bad:**

```
Project A needs FastAPI 0.100.0
Project B needs FastAPI 0.68.0

Without venv: ❌ Can't have both!
With venv: ✅ Each project has its own FastAPI
```

---

## 📊 Comparison: Node.js vs Python

| Node.js | Python |
|---------|--------|
| `node_modules/` in each project | `venv/` in each project |
| `npm install` = local | `pip install` = global by default |
| `package.json` = deps list | `requirements.txt` = deps list |
| Always isolated by default | Must explicitly isolate |

---

## 🔷 The Options

### 1. **venv** (Built-in, Recommended for beginners)

**Pros:**
- ✅ Built into Python (no install needed)
- ✅ Simple, lightweight
- ✅ Standard since Python 3.3
- ✅ Works everywhere

**Cons:**
- ❌ No lock file (versions can drift)
- ❌ Manual dependency management

**Best for:** Learning, simple projects, development

---

### 2. **conda** (Data Science Standard)

**Pros:**
- ✅ Manages Python version itself
- ✅ Great for data science (NumPy, pandas, PyTorch)
- ✅ Binary packages (fast install)

**Cons:**
- ❌ Heavy (500MB+ download)
- ❌ Separate install required
- ❌ Overkill for web dev

**Best for:** Data science, ML, AI projects

---

### 3. **poetry** (Modern, My Recommendation)

**Pros:**
- ✅ Lock file (like package-lock.json)
- ✅ Great dependency resolution
- ✅ Built-in packaging
- ✅ Nice CLI

**Cons:**
- ❌ Separate install (`pip install poetry`)
- ❌ Slightly more complex than venv

**Best for:** Production apps, libraries, serious projects

---

### 4. **pipenv** (Heroku's choice)

**Pros:**
- ✅ Combines pip + venv
- ✅ Lock file support
- ✅ Popular (Heroku supports it)

**Cons:**
- ❌ Can be slow
- ❌ Development slowed down
- ❌ Less popular than Poetry

**Best for:** Heroku deployment

---

## 🎯 My Recommendation: Start with venv

**For your learning/goals:**

```
Phase 1 (Now): venv
    ↓ Learn FastAPI, build projects
Phase 2 (Later): Poetry
    ↓ When building production apps
```

**Why start with venv?**
- No extra install (built-in!)
- Simple to learn
- Poetry adds concepts you don't need yet

---

## 🚀 venv: Quick Start

### Create a virtual environment:

```bash
cd my-project
python3 -m venv .venv
```

**What this creates:**
```
my-project/
├── .venv/              ← Isolated Python environment
│   ├── bin/            ← executables (python, pip)
│   ├── lib/            ← installed packages
│   └── ...             ← venv config
└── your code
```

---

### Activate it:

**Mac/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Your prompt changes:**
```bash
(.venv) $               ← See this? It's active!
```

---

### Install packages:

```bash
pip install fastapi uvicorn
```

**Now they're ONLY in `.venv`, not global!**

---

### Save dependencies:

```bash
pip freeze > requirements.txt
```

**Creates `requirements.txt`:**
```
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
```

---

### Deactivate:

```bash
deactivate
```

**Prompt changes back:**
```bash
$                      ← No (.venv) = deactivated
```

---

## 🔄 Typical Workflow

```bash
# 1. Create project
mkdir my-project && cd my-project

# 2. Create venv
python3 -m venv .venv

# 3. Activate
source .venv/bin/activate

# 4. Install packages
pip install fastapi uvicorn

# 5. Save dependencies
pip freeze > requirements.txt

# 6. Work on code...
# (your code here)

# 7. When done, deactivate
deactivate

# LATER: On another machine
git clone repo
cd repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt    # Install everything!
```

---

## 📦 venv Commands Reference

| Command | What it does |
|---------|--------------|
| `python3 -m venv .venv` | Create virtual env |
| `source .venv/bin/activate` | Activate (Mac/Linux) |
| `.venv\Scripts\activate` | Activate (Windows) |
| `deactivate` | Deactivate |
| `pip install package` | Install to venv |
| `pip freeze` | List installed packages |
| `pip freeze > requirements.txt` | Save dependencies |
| `pip install -r requirements.txt` | Install from file |

---

## 🎯 What About .gitignore?

**NEVER commit `.venv/`!**

**Add to `.gitignore`:**
```
.venv/
__pycache__/
*.pyc
```

**Why?**
- `.venv/` = 100MB+ of binaries
- `requirements.txt` = Tiny text file
- Everyone recreates `.venv/` from `requirements.txt`

---

## 🚀 Next: Poetry (When You're Ready)

**Once comfortable with venv, try Poetry:**

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create project
poetry new my-project
cd my-project

# Add packages
poetry add fastapi uvicorn

# Run in venv automatically
poetry run python main.py
```

**Poetry advantages:**
- `poetry.lock` = Exact versions (like package-lock.json)
- `pyproject.toml` = Modern config (like package.json)
- Auto-activates venv
- Better dependency resolution

---

## ✅ Summary

| For learning | For production |
|--------------|----------------|
| **venv** | **Poetry** |
| Built-in | Lock files |
| Simple | Better deps |
| Start here | Use later |

---

## 🎯 Your Next Steps

1. **Create venv for fastapi-basics:**
   ```bash
   cd fastapi-basics
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install FastAPI:**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Save dependencies:**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Confirm it works:**
   ```bash
   python --version        # Should show Python from .venv
   pip list                 # Should show fastapi, uvicorn
   ```

---

**Type "done" when you've created and activated your venv!**
