from sqlalchemy.orm import Session
from myapp.models.meal_plan import MealPlan

def create_meal_plan(db: Session, user_id: int, week: int, plan: str) -> MealPlan:
    new_plan = MealPlan(user_id=user_id, week=week, plan=plan)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

def get_meal_plan(db: Session, plan_id: int) -> MealPlan | None:
    return db.query(MealPlan).filter(MealPlan.id == plan_id).first()

def get_meal_plans_by_user(db: Session, user_id: int) -> list[MealPlan]:
    return db.query(MealPlan).filter(MealPlan.user_id == user_id).all()

def update_meal_plan(db: Session, plan_id: int, week: int | None = None, plan: str | None = None) -> MealPlan | None:
    meal_plan = get_meal_plan(db, plan_id)
    if not meal_plan:
        return None
    if week is not None:
        meal_plan.week = week
    if plan is not None:
        meal_plan.plan = plan
    db.commit()
    db.refresh(meal_plan)
    return meal_plan

def delete_meal_plan(db: Session, plan_id: int) -> bool:
    meal_plan = get_meal_plan(db, plan_id)
    if not meal_plan:
        return False
    db.delete(meal_plan)
    db.commit()
    return True
