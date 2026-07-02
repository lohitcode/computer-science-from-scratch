# FastAPI CRUD with SQLite/PostgreSQL

Complete CRUD application with FastAPI, SQLAlchemy, and Pydantic.

**Currently configured for SQLite (built-in, no setup needed!)**

---

## 📁 Project Structure

```
fastapi-crud/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & router setup
│   ├── database.py          # DB connection & session
│   ├── models.py            # SQLAlchemy models (DB tables)
│   ├── schemas.py           # Pydantic models (API validation)
│   ├── crud.py              # CRUD operations
│   ├── core/
│   │   └── config.py        # Settings
│   └── routers/
│       ├── users.py         # User routes
│       └── items.py         # Item routes
├── requirements.txt
└── .env
```

---

## 🚀 Quick Start (SQLite)

### 1. Create Virtual Environment

```bash
cd fastapi-crud
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

**Visit:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

**That's it!** SQLite database file (`fastapi.db`) will be created automatically.

---

## 📊 API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/` | Create user |
| GET | `/users/` | Get all users |
| GET | `/users/{id}` | Get user by ID |
| PATCH | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items/` | Create item |
| GET | `/items/` | Get all items |
| GET | `/items/search?q=` | Search items |
| GET | `/items/{id}` | Get item by ID |
| GET | `/items/owner/{id}` | Get items by owner |
| PATCH | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |

---

## 🧪 Test in Swagger Docs

1. Visit http://localhost:8000/docs
2. Try creating a user:
   ```json
   {
     "email": "john@example.com",
     "name": "John Doe",
     "password": "secret123"
   }
   ```
3. Try creating an item (with owner_id from created user)

---

## 🐳 Using PostgreSQL Instead (Optional)

If you have Docker installed:

1. **Install Docker Desktop:** https://www.docker.com/products/docker-desktop/

2. **Update `.env`:**
   ```
   DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydb
   ```

3. **Start PostgreSQL:**
   ```bash
   docker-compose up -d
   ```

**Same code, different database!** SQLAlchemy handles the difference.

---

## 📝 Best Practices Used

1. **Separation of concerns:**
   - `models.py` = Database tables
   - `schemas.py` = API validation
   - `crud.py` = Database operations
   - `routers/` = API endpoints

2. **Dependency injection:**
   - `get_db()` provides DB sessions
   - `Depends(get_db)` in routes

3. **Type hints:**
   - All functions have type hints
   - Response models validate output

4. **Status codes:**
   - 201 for creation
   - 204 for deletion
   - 404 for not found
   - 400 for bad requests

---

## 🗄️ Database Schema

### Users Table
- `id` (primary key)
- `email` (unique, indexed)
- `name`
- `hashed_password`
- `is_active`
- `created_at`, `updated_at`

### Items Table
- `id` (primary key)
- `title` (indexed)
- `description`
- `owner_id` (foreign key to users)
- `is_active`
- `created_at`

---

## ✅ What You're Learning

- **SQLAlchemy ORM** - Most widely used Python ORM
- **Pydantic** - Separate API validation from DB models
- **FastAPI dependency injection** - `Depends(get_db)` pattern
- **CRUD operations** - Create, Read, Update, Delete
- **Proper project structure** - How to organize FastAPI apps

---

## 🔄 SQLite vs PostgreSQL

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup** | None (built-in) | Docker/install required |
| **Use case** | Development, learning | Production |
| **Code changes** | None | Just DATABASE_URL |
| **Features** | Basic SQL | Full SQL features |

**Your code works with both!** Just change `DATABASE_URL` in `.env`.

---

**Run it now:**
```bash
cd fastapi-crud
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
