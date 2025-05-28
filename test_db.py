from myapp.db.database import Base, engine, SessionLocal
from datetime import date
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan

# ...

with SessionLocal() as session:
    # Create user
    new_user = User(name="Bob")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Add FoodEntry linked to new_user
    food_entry = FoodEntry(
        user_id=new_user.id,
        food="Apple",
        calories=95,
        date=date.today()
    )
    session.add(food_entry)

    # Add Goal linked to new_user
    goal = Goal(
        user_id=new_user.id,
        daily=2000,
        weekly=14000
    )
    session.add(goal)

    # Add MealPlan linked to new_user
    meal_plan = MealPlan(
        user_id=new_user.id,
        week=22,
        plan="Low-carb diet plan"
    )
    session.add(meal_plan)

    session.commit()

    # Query and print
    session.refresh(food_entry)
    session.refresh(goal)
    session.refresh(meal_plan)

    print(f"FoodEntry added: {food_entry.food} ({food_entry.calories} cal) for user {new_user.name}")
    print(f"Goal added: daily {goal.daily} cal, weekly {goal.weekly} cal for user {new_user.name}")
    print(f"MealPlan added: week {meal_plan.week}, plan: {meal_plan.plan} for user {new_user.name}")
