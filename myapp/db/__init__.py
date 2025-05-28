from .database import Base, engine, SessionLocal
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan

def init_db():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print(" Done.")

if __name__ == "__main__":
    init_db()
