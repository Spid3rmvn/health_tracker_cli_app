# myapp/controllers/report_controller.py

from sqlalchemy.orm import Session
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from datetime import date

def generate_user_report(db: Session, user_id: int, start_date: date, end_date: date):
    entries = db.query(FoodEntry).filter(
        FoodEntry.user_id == user_id,
        FoodEntry.date >= start_date,
        FoodEntry.date <= end_date
    ).all()

    print(f"DEBUG: Found {len(entries)} entries for user_id {user_id} between {start_date} and {end_date}")

    total_calories = sum(entry.calories for entry in entries)
    print(f"DEBUG: Total calories computed: {total_calories}")

    return {
        "user_id": user_id,
        "total_entries": len(entries),
        "total_calories": total_calories,
        "start_date": start_date,
        "end_date": end_date
    }
