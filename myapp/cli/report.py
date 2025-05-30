import typer
from datetime import datetime
from myapp.db.db import get_db
from myapp.controllers.report_controller import generate_user_report

app = typer.Typer(help="Report generation commands")

@app.command()
def user_report(
    user_id: int = typer.Argument(..., help="ID of the user"),
    start_date: str = typer.Argument(..., help="Start date in YYYY-MM-DD format"),
    end_date: str = typer.Argument(..., help="End date in YYYY-MM-DD format")
):
    """Generate a nutrition report for a user within a date range."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("❌ Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit(code=1)

    with get_db() as db:
        report = generate_user_report(db, user_id, start, end)

    if not report or report['total_entries'] == 0:
        typer.echo(f"📋 Report for User ID {user_id} from {start} to {end}:")
        typer.echo("No food entries found for this period.")
        return

    typer.echo(f"📋 Report for User ID {user_id} from {start} to {end}:")
    typer.echo(f"Total entries: {report['total_entries']}")
    typer.echo(f"Total calories: {report['total_calories']:,}")

if __name__ == "__main__":
    app()
