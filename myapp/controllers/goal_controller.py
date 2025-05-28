
from sqlalchemy.orm import Session
from myapp.models.goal import Goal

def create_goal(db: Session, user_id: int, daily: int, weekly: int) -> Goal:
    new_goal = Goal(user_id=user_id, daily=daily, weekly=weekly)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

def get_goal(db: Session, goal_id: int) -> Goal | None:
    return db.query(Goal).filter(Goal.id == goal_id).first()

def get_goals_by_user(db: Session, user_id: int) -> list[Goal]:
    return db.query(Goal).filter(Goal.user_id == user_id).all()

def update_goal(db: Session, goal_id: int, daily: int | None = None, weekly: int | None = None) -> Goal | None:
    goal = get_goal(db, goal_id)
    if not goal:
        return None
    if daily is not None:
        goal.daily = daily
    if weekly is not None:
        goal.weekly = weekly
    db.commit()
    db.refresh(goal)
    return goal

def delete_goal(db: Session, goal_id: int) -> bool:
    goal = get_goal(db, goal_id)
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True
