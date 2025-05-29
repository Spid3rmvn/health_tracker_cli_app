import typer
from myapp.cli import user, food, goal, meal_plan, report

app = typer.Typer()

app.add_typer(user.app, name="user")
app.add_typer(food.app, name="food")
app.add_typer(goal.app, name="goal")
app.add_typer(meal_plan.app, name="meal-plan")
app.add_typer(report.app, name="report")

if __name__ == "__main__":
    app()
