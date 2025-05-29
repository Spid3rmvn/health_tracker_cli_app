from sqlalchemy.orm import Session
from datetime import date
from myapp.models.food_entry import FoodEntry

def create_food_entry(db: Session, user_id: int, food: str, calories: int, entry_date: date) -> FoodEntry:
    new_entry = FoodEntry(user_id=user_id, food=food, calories=calories, date=entry_date)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry

def get_food_entry(db: Session, entry_id: int) -> FoodEntry | None:
    return db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()

def get_food_entries_by_user(db: Session, user_id: int) -> list[FoodEntry]:
    return db.query(FoodEntry).filter(FoodEntry.user_id == user_id).all()

def update_food_entry(db: Session, entry_id: int, food: str | None = None, calories: int | None = None, entry_date: date | None = None) -> FoodEntry | None:
    entry = get_food_entry(db, entry_id)
    if not entry:
        return None
    if food is not None:
        entry.food = food
    if calories is not None:
        entry.calories = calories
    if entry_date is not None:
        entry.date = entry_date
    db.commit()
    db.refresh(entry)
    return entry

def delete_food_entry(db: Session, entry_id: int) -> bool:
    entry = get_food_entry(db, entry_id)
    if not entry:
        return False
    db.delete(entry)
    db.commit()
    return True