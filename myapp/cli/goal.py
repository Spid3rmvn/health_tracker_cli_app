import typer
from typing import Optional
from myapp.controllers.goal_controller import (
    create_goal, get_goals_by_user, update_goal, delete_goal
)
from myapp.db.db import get_db

app = typer.Typer()

@app.command()
def add_goal(user_id: int, daily: int, weekly: int):
    with get_db() as db:
        goal = create_goal(db, user_id, daily, weekly)
        typer.echo(f"Goal created with ID {goal.id}")

@app.command()
def list_goals(user_id: int):
    with get_db() as db:
        goals = get_goals_by_user(db, user_id)
        for goal in goals:
            typer.echo(f"ID: {goal.id}, Daily: {goal.daily}, Weekly: {goal.weekly}")

@app.command()
def update_goal_cmd(goal_id: int, daily: Optional[int] = None, weekly: Optional[int] = None):
    with get_db() as db:
        updated = update_goal(db, goal_id, daily, weekly)
        if updated:
            typer.echo(f"Updated goal ID {goal_id}")
        else:
            typer.echo("Goal not found")

@app.command()
def delete_goal_cmd(goal_id: int):
    with get_db() as db:
        success = delete_goal(db, goal_id)
        typer.echo("Goal deleted" if success else "Goal not found")
if __name__ == "__main__":
    app()
