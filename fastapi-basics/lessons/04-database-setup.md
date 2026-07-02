# Lesson 4: Database with FastAPI + PostgreSQL

## 🎯 The Stack (Industry Standard)

| Component | Tool | Why |
|-----------|------|-----|
| **Database** | PostgreSQL | Most popular for production |
| **ORM** | SQLAlchemy | Most widely used Python ORM |
| **Migrations** | Alembic | Standard migration tool |
| **Container** | Docker Compose | Local development |

---

## 📁 Project Structure

```
fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic models (API)
│   ├── crud.py              # Database operations
│   ├── routers/             # Route modules
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   └── core/                # Config
│       ├── __init__.py
│       └── config.py
├── alembic/                 # Migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── docker-compose.yml       # PostgreSQL container
├── requirements.txt
└── .env                     # Environment variables
```

---

## 🐳 Docker Compose (PostgreSQL)

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    container_name: fastapi_db
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Run it:**
```bash
docker-compose up -d
```

---

## 🔧 Database Connection

**app/database.py:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL from environment variable
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/mydb"

# Create engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 📦 SQLAlchemy Models (Database Tables)

**app/models.py:**
```python
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
```

---

## 🔮 Pydantic Schemas (API Models)

**app/schemas.py:**
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # SQLAlchemy → Pydantic
```

---

## 🔄 CRUD Operations

**app/crud.py:**
```python
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from hashing import Hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    # Hash password first!
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
```

---

## 🛣️ Routes

**app/routers/users.py:**
```python
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, models

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
```

---

## 📊 Migrations with Alembic

**Install:**
```bash
pip install alembic
```

**Initialize:**
```bash
alembic init alembic
```

**Configure alembic/env.py:**
```python
# Add at top
from app.database import Base
from app.models import User  # Import all models

target_metadata = Base.metadata
```

**Create migration:**
```bash
alembic revision --autogenerate -m "Create users table"
```

**Run migration:**
```bash
alembic upgrade head
```

---

## 📋 requirements.txt

```
fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary
python-dotenv
pydantic[email]
```

---

## ✅ Workflow

1. **Start PostgreSQL:** `docker-compose up -d`
2. **Create model** in `models.py`
3. **Generate migration:** `alembic revision --autogenerate`
4. **Run migration:** `alembic upgrade head`
5. **Create CRUD** functions
6. **Create routes** with Pydantic schemas

---

## 🎯 Key Best Practices

1. **Separate models:** SQLAlchemy (DB) vs Pydantic (API)
2. **Use dependency injection:** `Depends(get_db)`
3. **Always use migrations:** Never modify DB directly
4. **Hash passwords:** Never store plain text
5. **Use indexes:** For columns queried often
6. **Validate with Pydantic:** Before DB operations

---

**Next: Let's build this step by step!**
