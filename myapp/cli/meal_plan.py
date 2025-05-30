import typer
from typing import Optional
from myapp.controllers.meal_plan_controller import (
    create_meal_plan, get_meal_plans_by_user, update_meal_plan, delete_meal_plan
)
from myapp.db.db import get_db

app = typer.Typer(help="Meal planning commands")

@app.command()
def add_meal_plan(
    user_id: int = typer.Argument(..., help="ID of the user"),
    week: int = typer.Argument(..., help="Week number for the meal plan"),
    plan: str = typer.Argument(..., help="Meal plan description")
):
    """Create a new meal plan for a user."""
    with get_db() as db:
        mp = create_meal_plan(db, user_id, week, plan)
        typer.echo(f"Meal plan created with ID {mp.id}")

@app.command()
def list_meal_plans(user_id: int = typer.Argument(..., help="ID of the user")):
    """List all meal plans for a user."""
    with get_db() as db:
        plans = get_meal_plans_by_user(db, user_id)
        for p in plans:
            typer.echo(f"ID: {p.id}, Week: {p.week}, Plan: {p.plan}")

@app.command()
def update_meal_plan_cmd(
    plan_id: int = typer.Argument(..., help="ID of the meal plan to update"),
    week: Optional[int] = typer.Option(None, "--week", help="New week number"),
    plan: Optional[str] = typer.Option(None, "--plan", help="New meal plan description")
):
    """Update an existing meal plan."""
    with get_db() as db:
        updated = update_meal_plan(db, plan_id, week, plan)
        if updated:
            typer.echo(f"Updated meal plan ID {plan_id}")
        else:
            typer.echo("Meal plan not found")

@app.command()
def delete_meal_plan_cmd(plan_id: int = typer.Argument(..., help="ID of the meal plan to delete")):
    """Delete a meal plan."""
    with get_db() as db:
        success = delete_meal_plan(db, plan_id)
        typer.echo("Meal plan deleted" if success else "Meal plan not found")

if __name__ == "__main__":
    app()