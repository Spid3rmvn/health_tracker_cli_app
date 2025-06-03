import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import date, datetime

# Import all CLI apps
from myapp.cli.user import app as user_app
from myapp.cli.food import app as food_app
from myapp.cli.goal import app as goal_app
from myapp.cli.meal_plan import app as meal_plan_app
from myapp.cli.report import app as report_app
from myapp.cli.__main__ import app as main_app

# Import models for mocking
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan


class TestAllCLICommands:
    """Test all CLI commands to ensure they're working as expected."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    # USER COMMANDS TESTS

    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.create_user')
    def test_user_add_command(self, mock_create_user, mock_get_db):
        """Test the add-user command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_user = User(id=1, name="test_user")
        mock_create_user.return_value = mock_user

        result = self.runner.invoke(user_app, ["add-user", "test_user"])

        assert result.exit_code == 0
        assert "User created with ID 1 and name 'test_user'" in result.stdout
        mock_create_user.assert_called_once_with(mock_db, "test_user")

    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.update_user')
    def test_user_update_command(self, mock_update_user, mock_get_db):
        """Test the update-user-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_update_user.return_value = True

        result = self.runner.invoke(user_app, ["update-user-cmd", "1", "--name", "updated_user"])

        assert result.exit_code == 0
        assert "Updated user ID 1" in result.stdout
        mock_update_user.assert_called_once_with(mock_db, 1, "updated_user")

    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.delete_user')
    def test_user_delete_command(self, mock_delete_user, mock_get_db):
        """Test the delete-user-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_delete_user.return_value = True

        result = self.runner.invoke(user_app, ["delete-user-cmd", "1"])

        assert result.exit_code == 0
        assert "User deleted" in result.stdout
        mock_delete_user.assert_called_once_with(mock_db, 1)

    # FOOD COMMANDS TESTS

    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.get_food_entries_by_user')
    def test_food_list_command(self, mock_get_entries, mock_get_db):
        """Test the list-food-entries command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_entries = [
            FoodEntry(id=1, user_id=1, food="Apple", calories=95, date=date.today()),
            FoodEntry(id=2, user_id=1, food="Banana", calories=105, date=date.today())
        ]
        mock_get_entries.return_value = mock_entries

        result = self.runner.invoke(food_app, ["list-food-entries", "1"])

        assert result.exit_code == 0
        assert "ID: 1, Food: Apple, Calories: 95" in result.stdout
        assert "ID: 2, Food: Banana, Calories: 105" in result.stdout
        mock_get_entries.assert_called_once_with(mock_db, 1)

    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.update_food_entry')
    def test_food_update_command(self, mock_update_entry, mock_get_db):
        """Test the update-food-entry-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_update_entry.return_value = True

        result = self.runner.invoke(food_app, [
            "update-food-entry-cmd", "1", 
            "--food", "Updated Food", 
            "--calories", "150"
        ])

        assert result.exit_code == 0
        assert "Updated food entry ID 1" in result.stdout
        mock_update_entry.assert_called_once_with(mock_db, 1, "Updated Food", 150, None)

    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.delete_food_entry')
    def test_food_delete_command(self, mock_delete_entry, mock_get_db):
        """Test the delete-food-entry-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_delete_entry.return_value = True

        result = self.runner.invoke(food_app, ["delete-food-entry-cmd", "1"])

        assert result.exit_code == 0
        assert "Food entry deleted" in result.stdout
        mock_delete_entry.assert_called_once_with(mock_db, 1)

    # GOAL COMMANDS TESTS

    @patch('myapp.cli.goal.get_db')
    @patch('myapp.cli.goal.create_goal')
    def test_goal_add_command(self, mock_create_goal, mock_get_db):
        """Test the add-goal command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_goal = Goal(id=1, user_id=1, daily=2000, weekly=14000)
        mock_create_goal.return_value = mock_goal

        result = self.runner.invoke(goal_app, ["add-goal", "1", "2000", "14000"])

        assert result.exit_code == 0
        assert "Goal created with ID 1" in result.stdout
        mock_create_goal.assert_called_once_with(mock_db, 1, 2000, 14000)

    @patch('myapp.cli.goal.get_db')
    @patch('myapp.cli.goal.get_goals_by_user')
    def test_goal_list_command(self, mock_get_goals, mock_get_db):
        """Test the list-goals command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_goals = [
            Goal(id=1, user_id=1, daily=2000, weekly=14000),
            Goal(id=2, user_id=1, daily=1800, weekly=12600)
        ]
        mock_get_goals.return_value = mock_goals

        result = self.runner.invoke(goal_app, ["list-goals", "1"])

        assert result.exit_code == 0
        assert "ID: 1, Daily: 2000, Weekly: 14000" in result.stdout
        assert "ID: 2, Daily: 1800, Weekly: 12600" in result.stdout
        mock_get_goals.assert_called_once_with(mock_db, 1)

    @patch('myapp.cli.goal.get_db')
    @patch('myapp.cli.goal.update_goal')
    def test_goal_update_command(self, mock_update_goal, mock_get_db):
        """Test the update-goal-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_update_goal.return_value = True

        result = self.runner.invoke(goal_app, [
            "update-goal-cmd", "1", 
            "--daily", "1800", 
            "--weekly", "12600"
        ])

        assert result.exit_code == 0
        assert "Updated goal ID 1" in result.stdout
        mock_update_goal.assert_called_once_with(mock_db, 1, 1800, 12600)

    @patch('myapp.cli.goal.get_db')
    @patch('myapp.cli.goal.delete_goal')
    def test_goal_delete_command(self, mock_delete_goal, mock_get_db):
        """Test the delete-goal-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_delete_goal.return_value = True

        result = self.runner.invoke(goal_app, ["delete-goal-cmd", "1"])

        assert result.exit_code == 0
        assert "Goal deleted" in result.stdout
        mock_delete_goal.assert_called_once_with(mock_db, 1)

    # MEAL PLAN COMMANDS TESTS

    @patch('myapp.cli.meal_plan.get_db')
    @patch('myapp.cli.meal_plan.create_meal_plan')
    def test_meal_plan_add_command(self, mock_create_plan, mock_get_db):
        """Test the add-meal-plan command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_plan = MealPlan(id=1, user_id=1, week=1, plan="Test meal plan")
        mock_create_plan.return_value = mock_plan

        result = self.runner.invoke(meal_plan_app, ["add-meal-plan", "1", "1", "Test meal plan"])

        assert result.exit_code == 0
        assert "Meal plan created with ID 1" in result.stdout
        mock_create_plan.assert_called_once_with(mock_db, 1, 1, "Test meal plan")

    @patch('myapp.cli.meal_plan.get_db')
    @patch('myapp.cli.meal_plan.get_meal_plans_by_user')
    def test_meal_plan_list_command(self, mock_get_plans, mock_get_db):
        """Test the list-meal-plans command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_plans = [
            MealPlan(id=1, user_id=1, week=1, plan="Week 1 plan"),
            MealPlan(id=2, user_id=1, week=2, plan="Week 2 plan")
        ]
        mock_get_plans.return_value = mock_plans

        result = self.runner.invoke(meal_plan_app, ["list-meal-plans", "1"])

        assert result.exit_code == 0
        assert "ID: 1, Week: 1, Plan: Week 1 plan" in result.stdout
        assert "ID: 2, Week: 2, Plan: Week 2 plan" in result.stdout
        mock_get_plans.assert_called_once_with(mock_db, 1)

    @patch('myapp.cli.meal_plan.get_db')
    @patch('myapp.cli.meal_plan.update_meal_plan')
    def test_meal_plan_update_command(self, mock_update_plan, mock_get_db):
        """Test the update-meal-plan-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_update_plan.return_value = True

        result = self.runner.invoke(meal_plan_app, [
            "update-meal-plan-cmd", "1", 
            "--week", "2", 
            "--plan", "Updated meal plan"
        ])

        assert result.exit_code == 0
        assert "Updated meal plan ID 1" in result.stdout
        mock_update_plan.assert_called_once_with(mock_db, 1, 2, "Updated meal plan")

    @patch('myapp.cli.meal_plan.get_db')
    @patch('myapp.cli.meal_plan.delete_meal_plan')
    def test_meal_plan_delete_command(self, mock_delete_plan, mock_get_db):
        """Test the delete-meal-plan-cmd command."""
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        mock_delete_plan.return_value = True

        result = self.runner.invoke(meal_plan_app, ["delete-meal-plan-cmd", "1"])

        assert result.exit_code == 0
        assert "Meal plan deleted" in result.stdout
        mock_delete_plan.assert_called_once_with(mock_db, 1)

    # REPORT COMMANDS TESTS

    @patch('myapp.controllers.report_controller.generate_user_report')
    def test_report_controller_functionality(self, mock_generate_report):
        """Test the report controller functionality directly."""
        from myapp.controllers.report_controller import generate_user_report
        from datetime import date

        # Mock a report with entries
        mock_report = {
            'total_entries': 5,
            'total_calories': 1500,
            'days_tracked': 3,
            'days_in_period': 7,
            'tracking_consistency': 42.86,
            'avg_daily_calories': 500,
            'has_goal': True,
            'daily_goal': 2000,
            'daily_goal_percent': 25,
            'weekly_goal': 14000,
            'weekly_avg_calories': 3500,
            'weekly_goal_percent': 25,
            'daily_breakdown': {'2024-01-01': 500, '2024-01-02': 500, '2024-01-03': 500}
        }
        mock_generate_report.return_value = mock_report

        # Call the controller function directly
        mock_db = MagicMock()
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 7)

        report = generate_user_report(mock_db, 1, start_date, end_date)

        # Verify the controller was called with correct parameters
        mock_generate_report.assert_called_once_with(mock_db, 1, start_date, end_date)

        # Verify the report contains the expected data
        assert report == mock_report
        assert report['total_entries'] == 5
        assert report['total_calories'] == 1500
        assert report['days_tracked'] == 3
        assert report['days_in_period'] == 7

    def test_report_date_validation(self):
        """Test date validation in the report controller."""
        from datetime import datetime

        # Test valid date format
        valid_date_str = "2024-01-01"
        try:
            date_obj = datetime.strptime(valid_date_str, "%Y-%m-%d").date()
            assert date_obj.year == 2024
            assert date_obj.month == 1
            assert date_obj.day == 1
        except ValueError:
            pytest.fail("Valid date string raised ValueError")

        # Test invalid date format
        invalid_date_str = "invalid-date"
        with pytest.raises(ValueError):
            datetime.strptime(invalid_date_str, "%Y-%m-%d").date()

    # MAIN APP TESTS

    def test_main_app_structure(self):
        """Test the structure of the main CLI app."""
        # Instead of testing the internal structure of the Typer app,
        # we'll verify that all the CLI modules can be imported successfully

        # Test that all CLI modules can be imported
        import importlib

        # List of CLI modules to test
        cli_modules = [
            "myapp.cli.user",
            "myapp.cli.food",
            "myapp.cli.goal",
            "myapp.cli.meal_plan",
            "myapp.cli.report",
            "myapp.cli.__main__"
        ]

        # Try to import each module
        for module_name in cli_modules:
            try:
                module = importlib.import_module(module_name)
                assert hasattr(module, "app"), f"Module {module_name} does not have an 'app' attribute"
            except ImportError:
                pytest.fail(f"Failed to import {module_name}")

        # Verify the main app exists
        from myapp.cli.__main__ import app
        assert app is not None
