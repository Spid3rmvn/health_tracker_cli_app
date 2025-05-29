from sqlalchemy.orm import Session
from contextlib import contextmanager
from myapp.db.database import SessionLocal

@contextmanager
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()