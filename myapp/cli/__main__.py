import typer
from myapp.cli import user, food, goal, meal_plan, report

app = typer.Typer(
    name="health-tracker",
    help="Health Tracker CLI - Track your nutrition and fitness goals",
    no_args_is_help=True
)

app.add_typer(user.app, name="user", help="User management commands")
app.add_typer(food.app, name="food", help="Food tracking commands")
app.add_typer(goal.app, name="goal", help="Goal management commands")
app.add_typer(meal_plan.app, name="meal-plan", help="Meal planning commands")
app.add_typer(report.app, name="report", help="Report generation commands")

if __name__ == "__main__":
    app()
