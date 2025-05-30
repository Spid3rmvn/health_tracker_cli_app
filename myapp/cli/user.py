import typer
from typing import Optional
from sqlalchemy.orm import Session
from myapp.controllers.user_controller import (
    create_user, get_user_by_name, get_all_users, update_user, delete_user
)
from myapp.db.db import get_db

app = typer.Typer()

@app.command()
def add_user(name: str):
    with get_db() as db:
        user = create_user(db, name)
        typer.echo(f"User created with ID {user.id} and name '{user.name}'")

@app.command()
def get_user(name: str):
    with get_db() as db:
        user = get_user_by_name(db, name)
        if user:
            typer.echo(f"ID: {user.id}, Name: {user.name}")
        else:
            typer.echo("User not found")

@app.command()
def list_users():
    with get_db() as db:
        users = get_all_users(db)
        for user in users:
            typer.echo(f"ID: {user.id}, Name: {user.name}")

@app.command()
def update_user_cmd(user_id: int, name: Optional[str] = None):
    with get_db() as db:
        updated = update_user(db, user_id, name)
        if updated:
            typer.echo(f"Updated user ID {user_id} to name '{updated.name}'")
        else:
            typer.echo("User not found")

@app.command()
def delete_user_cmd(user_id: int):
    with get_db() as db:
        success = delete_user(db, user_id)
        typer.echo("User deleted" if success else "User not found")


if __name__ == "__main__":
    app()