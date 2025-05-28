
from sqlalchemy.orm import Session
from myapp.models.user import User

def create_user(db: Session, name: str) -> User:
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_name(db: Session, name: str) -> User | None:
    return db.query(User).filter(User.name == name).first()

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

def update_user(db: Session, user_id: int, name: str | None = None) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None
    if name is not None:
        user.name = name
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
