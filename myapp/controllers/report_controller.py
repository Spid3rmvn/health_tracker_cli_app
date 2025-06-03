# myapp/controllers/report_controller.py

from sqlalchemy.orm import Session
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from datetime import date, timedelta
from collections import defaultdict

def generate_user_report(db: Session, user_id: int, start_date: date, end_date: date):
    # Get all food entries in the date range
    entries = db.query(FoodEntry).filter(
        FoodEntry.user_id == user_id,
        FoodEntry.date >= start_date,
        FoodEntry.date <= end_date
    ).all()

    # Get the user's most recent goal
    goal = db.query(Goal).filter(Goal.user_id == user_id).order_by(Goal.id.desc()).first()

    # Calculate total calories
    total_calories = sum(entry.calories for entry in entries)

    # Calculate days in the period
    days_in_period = (end_date - start_date).days + 1

    # Calculate days with entries
    days_with_entries = len(set(entry.date for entry in entries))

    # Calculate average daily calories
    avg_daily_calories = total_calories / days_with_entries if days_with_entries > 0 else 0

    # Group entries by date for daily breakdown
    daily_breakdown = defaultdict(int)
    for entry in entries:
        daily_breakdown[entry.date] += entry.calories

    # Sort the daily breakdown by date
    sorted_daily = {k.isoformat(): v for k, v in sorted(daily_breakdown.items())}

    # Prepare the report
    report = {
        "user_id": user_id,
        "total_entries": len(entries),
        "total_calories": total_calories,
        "start_date": start_date,
        "end_date": end_date,
        "days_in_period": days_in_period,
        "days_tracked": days_with_entries,
        "tracking_consistency": round(days_with_entries / days_in_period * 100, 1) if days_in_period > 0 else 0,
        "avg_daily_calories": round(avg_daily_calories, 1),
        "daily_breakdown": sorted_daily
    }

    # Add goal comparison if a goal exists
    if goal:
        report["has_goal"] = True
        report["daily_goal"] = goal.daily
        report["weekly_goal"] = goal.weekly

        # Calculate daily goal comparison
        if goal.daily > 0:
            report["daily_goal_percent"] = round(avg_daily_calories / goal.daily * 100, 1)

        # Calculate weekly average and goal comparison
        weekly_avg = total_calories / (days_in_period / 7) if days_in_period > 0 else 0
        report["weekly_avg_calories"] = round(weekly_avg, 1)

        if goal.weekly > 0:
            report["weekly_goal_percent"] = round(weekly_avg / goal.weekly * 100, 1)
    else:
        report["has_goal"] = False

    return report
