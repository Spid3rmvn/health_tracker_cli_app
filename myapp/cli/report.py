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

    # Display basic report information
    typer.echo(f"\n📋 NUTRITION REPORT for User ID {user_id}")
    typer.echo(f"📅 Period: {start} to {end} ({report['days_in_period']} days)")
    typer.echo("=" * 50)

    # Display summary statistics
    typer.echo("\n📊 SUMMARY STATISTICS")
    typer.echo(f"Total entries: {report['total_entries']}")
    typer.echo(f"Total calories: {report['total_calories']:,}")
    typer.echo(f"Days tracked: {report['days_tracked']} of {report['days_in_period']} ({report['tracking_consistency']}% consistency)")
    typer.echo(f"Average daily calories: {report['avg_daily_calories']:,}")

    # Display goal comparison if available
    if report.get('has_goal', False):
        typer.echo("\n🎯 GOAL COMPARISON")
        typer.echo(f"Daily calorie goal: {report['daily_goal']:,}")
        if 'daily_goal_percent' in report:
            goal_status = "✅ Under goal" if report['daily_goal_percent'] <= 100 else "❌ Over goal"
            typer.echo(f"Daily average: {report['avg_daily_calories']:,} calories ({report['daily_goal_percent']}% of goal) {goal_status}")

        typer.echo(f"Weekly calorie goal: {report['weekly_goal']:,}")
        if 'weekly_goal_percent' in report:
            weekly_goal_status = "✅ Under goal" if report['weekly_goal_percent'] <= 100 else "❌ Over goal"
            typer.echo(f"Weekly average: {report['weekly_avg_calories']:,} calories ({report['weekly_goal_percent']}% of goal) {weekly_goal_status}")

    # Display daily breakdown if requested
    if report.get('daily_breakdown') and len(report['daily_breakdown']) > 0:
        typer.echo("\n📆 DAILY BREAKDOWN")
        for date_str, calories in report['daily_breakdown'].items():
            typer.echo(f"{date_str}: {calories:,} calories")

if __name__ == "__main__":
    app()
