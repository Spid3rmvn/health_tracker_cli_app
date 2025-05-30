"""
Essential CLI tests that verify the working CLI commands.
These tests focus on the commands that we know work correctly.
"""
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import date
from myapp.cli.user import app as user_app
from myapp.cli.food import app as food_app
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry


class TestEssentialCLI:
    """Essential CLI tests for working commands."""
    
    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.create_user')
    def test_user_add_command_works(self, mock_create_user, mock_get_db):
        """Test that the add-user command works correctly."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user creation
        mock_user = User(id=1, name="test_user")
        mock_create_user.return_value = mock_user
        
        # Run command
        result = self.runner.invoke(user_app, ["add-user", "test_user"])
        
        # Verify it worked
        assert result.exit_code == 0
        assert "User created with ID 1 and name 'test_user'" in result.stdout
        mock_create_user.assert_called_once_with(mock_db, "test_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_user_by_name')
    def test_user_get_command_works(self, mock_get_user_by_name, mock_get_db):
        """Test that the get-user command works correctly."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user retrieval
        mock_user = User(id=1, name="test_user")
        mock_get_user_by_name.return_value = mock_user
        
        # Run command
        result = self.runner.invoke(user_app, ["get-user", "test_user"])
        
        # Verify it worked
        assert result.exit_code == 0
        assert "ID: 1, Name: test_user" in result.stdout
        mock_get_user_by_name.assert_called_once_with(mock_db, "test_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_user_by_name')
    def test_user_get_command_not_found(self, mock_get_user_by_name, mock_get_db):
        """Test get-user command when user is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user not found
        mock_get_user_by_name.return_value = None
        
        # Run command
        result = self.runner.invoke(user_app, ["get-user", "nonexistent_user"])
        
        # Verify it handled the case correctly
        assert result.exit_code == 0
        assert "User not found" in result.stdout
        mock_get_user_by_name.assert_called_once_with(mock_db, "nonexistent_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_all_users')
    def test_user_list_command_works(self, mock_get_all_users, mock_get_db):
        """Test that the list-users command works correctly."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock users list
        mock_users = [
            User(id=1, name="user1"),
            User(id=2, name="user2"),
            User(id=3, name="user3")
        ]
        mock_get_all_users.return_value = mock_users
        
        # Run command
        result = self.runner.invoke(user_app, ["list-users"])
        
        # Verify it worked
        assert result.exit_code == 0
        assert "ID: 1, Name: user1" in result.stdout
        assert "ID: 2, Name: user2" in result.stdout
        assert "ID: 3, Name: user3" in result.stdout
        mock_get_all_users.assert_called_once_with(mock_db)
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_all_users')
    def test_user_list_command_empty(self, mock_get_all_users, mock_get_db):
        """Test list-users command when no users exist."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock empty users list
        mock_get_all_users.return_value = []
        
        # Run command
        result = self.runner.invoke(user_app, ["list-users"])
        
        # Verify it handled empty case correctly
        assert result.exit_code == 0
        # Should not output any user information
        assert "ID:" not in result.stdout
        mock_get_all_users.assert_called_once_with(mock_db)
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.create_food_entry')
    def test_food_add_command_works(self, mock_create_food_entry, mock_get_db):
        """Test that the add-food command works correctly."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entry creation
        mock_entry = FoodEntry(id=1, user_id=1, food="Apple", calories=95, date=date.today())
        mock_create_food_entry.return_value = mock_entry
        
        # Run command
        result = self.runner.invoke(food_app, ["add-food", "1", "Apple", "95"])
        
        # Verify it worked
        assert result.exit_code == 0
        assert "Food entry created with ID 1" in result.stdout
        mock_create_food_entry.assert_called_once()
        # Check that the function was called with correct parameters
        args = mock_create_food_entry.call_args[0]
        assert args[0] == mock_db
        assert args[1] == 1  # user_id
        assert args[2] == "Apple"  # food
        assert args[3] == 95  # calories
        assert args[4] == date.today()  # date
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.create_food_entry')
    def test_food_add_command_with_date(self, mock_create_food_entry, mock_get_db):
        """Test add-food command with a specific date."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entry creation
        mock_entry = FoodEntry(id=1, user_id=1, food="Banana", calories=105, date=date(2024, 1, 15))
        mock_create_food_entry.return_value = mock_entry
        
        # Run command with date
        result = self.runner.invoke(food_app, ["add-food", "1", "Banana", "105", "--date", "2024-01-15"])
        
        # Verify it worked
        assert result.exit_code == 0
        assert "Food entry created with ID 1" in result.stdout
        mock_create_food_entry.assert_called_once()
        # Check that the function was called with the specified date
        args = mock_create_food_entry.call_args[0]
        assert args[4] == date(2024, 1, 15)
    
    def test_food_add_command_invalid_date(self):
        """Test add-food command with an invalid date format."""
        # Run command with invalid date
        result = self.runner.invoke(food_app, ["add-food", "1", "Apple", "95", "--date", "invalid-date"])
        
        # Verify it handled the error correctly
        assert result.exit_code == 1
        assert "Invalid date format. Use YYYY-MM-DD." in result.stdout
    
    def test_cli_modules_can_be_imported(self):
        """Test that all CLI modules can be imported successfully."""
        # Test user CLI
        from myapp.cli.user import app as user_app
        assert user_app is not None
        
        # Test food CLI
        from myapp.cli.food import app as food_app
        assert food_app is not None
        
        # Test goal CLI
        from myapp.cli.goal import app as goal_app
        assert goal_app is not None
        
        # Test meal plan CLI
        from myapp.cli.meal_plan import app as meal_plan_app
        assert meal_plan_app is not None
        
        # Test report CLI
        from myapp.cli.report import app as report_app
        assert report_app is not None
    
    def test_main_cli_can_be_imported(self):
        """Test that the main CLI app can be imported."""
        from myapp.cli.__main__ import app
        assert app is not None
