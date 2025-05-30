import typer
from typing import Optional
from datetime import datetime
from myapp.controllers.food_entry_controller import (
    create_food_entry, get_food_entries_by_user, update_food_entry, delete_food_entry
)
from myapp.db.db import get_db

app = typer.Typer()

@app.command()
def add_food(user_id: int, food: str, calories: int, date: Optional[str] = None):
    """Add a new food entry."""
    try:
        entry_date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.today().date()
    except ValueError:
        typer.echo("Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit(code=1)

    with (get_db()) as db:  # FIXED: wrap get_db() with next()
        entry = create_food_entry(db, user_id, food, calories, entry_date)
        typer.echo(f"Food entry created with ID {entry.id}")

@app.command()
def list_food_entries(user_id: int):
    """List all food entries for a user."""
    with (get_db()) as db:
        entries = get_food_entries_by_user(db, user_id)
        for e in entries:
            typer.echo(f"ID: {e.id}, Food: {e.food}, Calories: {e.calories}, Date: {e.date}")

@app.command()
def update_food_entr_cmd(entry_id: int, food: Optional[str] = None, calories: Optional[int] = None, date: Optional[str] = None):
    """Update an existing food entry."""
    entry_date = None
    if date:
        try:
            entry_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            typer.echo("Invalid date format. Use YYYY-MM-DD.")
            raise typer.Exit(code=1)

    with (get_db()) as db:
        updated = update_food_entry(db, entry_id, food, calories, entry_date)
        if updated:
            typer.echo(f"Updated food entry ID {entry_id}")
        else:
            typer.echo("Food entry not found")

@app.command()
def delete_food_entry_cmd(entry_id: int):
    """Delete a food entry."""
    with (get_db()) as db:
        success = delete_food_entry(db, entry_id)
        typer.echo("Food entry deleted" if success else "Food entry not found")

if __name__ == "__main__":
    app()
