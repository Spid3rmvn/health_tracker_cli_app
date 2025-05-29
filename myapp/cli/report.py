import typer
from datetime import datetime
from myapp.db.db import get_db
from myapp.controllers.report_controller import generate_user_report

app = typer.Typer()

@app.command()
def user_report(user_id: int, start_date: str, end_date: str):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit(code=1)

    with get_db() as db:
        typer.echo(f"Fetching report for user ID {user_id} between {start} and {end}...")
        report = generate_user_report(db, user_id, start, end)
        typer.echo(f"DEBUG: report = {report}")

    if not report or report['total_entries'] == 0:
        typer.echo(f"❌ No report found for user ID {user_id} between {start} and {end}")
        raise typer.Exit(code=1)

    typer.echo(f"📋 Report for User ID {user_id} from {start} to {end}:\n")
    typer.echo(f"Total entries: {report['total_entries']}")
    typer.echo(f"Total calories: {report['total_calories']}")

if __name__ == "__main__":
    app()
