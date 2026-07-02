from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
# For SQLite, we need check_same_thread=False
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

# SessionLocal factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()


# Dependency: Get DB session for routes
def get_db():
    """
    Yield a database session.

    Usage in route:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
