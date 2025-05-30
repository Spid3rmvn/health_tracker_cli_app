"""
Tests for the food CLI commands.
"""
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from datetime import date
from myapp.cli.food import app
from myapp.models.food_entry import FoodEntry


@pytest.mark.cli
class TestFoodCLI:
    """Test cases for food CLI commands."""
    
    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.create_food_entry')
    def test_add_food_command(self, mock_create_food_entry, mock_get_db):
        """Test the add-food command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entry creation
        mock_entry = FoodEntry(id=1, user_id=1, food="Apple", calories=95, date=date.today())
        mock_create_food_entry.return_value = mock_entry
        
        # Run command
        result = self.runner.invoke(app, ["add-food", "1", "Apple", "95"])
        
        # Assertions
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
    def test_add_food_command_with_date(self, mock_create_food_entry, mock_get_db):
        """Test the add-food command with a specific date."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entry creation
        mock_entry = FoodEntry(id=1, user_id=1, food="Banana", calories=105, date=date(2024, 1, 15))
        mock_create_food_entry.return_value = mock_entry
        
        # Run command with date
        result = self.runner.invoke(app, ["add-food", "1", "Banana", "105", "--date", "2024-01-15"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Food entry created with ID 1" in result.stdout
        mock_create_food_entry.assert_called_once()
        # Check that the function was called with the specified date
        args = mock_create_food_entry.call_args[0]
        assert args[4] == date(2024, 1, 15)
    
    def test_add_food_command_invalid_date(self):
        """Test the add-food command with an invalid date format."""
        # Run command with invalid date
        result = self.runner.invoke(app, ["add-food", "1", "Apple", "95", "--date", "invalid-date"])
        
        # Assertions
        assert result.exit_code == 1
        assert "Invalid date format. Use YYYY-MM-DD." in result.stdout
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.get_food_entries_by_user')
    def test_list_food_command(self, mock_get_food_entries_by_user, mock_get_db):
        """Test the list-food command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entries
        mock_entries = [
            FoodEntry(id=1, user_id=1, food="Apple", calories=95, date=date.today()),
            FoodEntry(id=2, user_id=1, food="Banana", calories=105, date=date.today()),
            FoodEntry(id=3, user_id=1, food="Orange", calories=62, date=date.today())
        ]
        mock_get_food_entries_by_user.return_value = mock_entries
        
        # Run command
        result = self.runner.invoke(app, ["list-food", "1"])
        
        # Assertions
        assert result.exit_code == 0
        assert "ID: 1, Food: Apple, Calories: 95" in result.stdout
        assert "ID: 2, Food: Banana, Calories: 105" in result.stdout
        assert "ID: 3, Food: Orange, Calories: 62" in result.stdout
        mock_get_food_entries_by_user.assert_called_once_with(mock_db, 1)
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.get_food_entries_by_user')
    def test_list_food_command_empty(self, mock_get_food_entries_by_user, mock_get_db):
        """Test the list-food command when no entries exist."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock empty entries list
        mock_get_food_entries_by_user.return_value = []
        
        # Run command
        result = self.runner.invoke(app, ["list-food", "1"])
        
        # Assertions
        assert result.exit_code == 0
        # Should not output any food entry information
        assert "ID:" not in result.stdout
        mock_get_food_entries_by_user.assert_called_once_with(mock_db, 1)
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.update_food_entry')
    def test_update_food_command(self, mock_update_food_entry, mock_get_db):
        """Test the update-food command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock food entry update
        mock_entry = FoodEntry(id=1, user_id=1, food="Updated Apple", calories=100, date=date.today())
        mock_update_food_entry.return_value = mock_entry
        
        # Run command
        result = self.runner.invoke(app, ["update-food", "1", "--food", "Updated Apple", "--calories", "100"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Updated food entry ID 1" in result.stdout
        mock_update_food_entry.assert_called_once()
        # Check that the function was called with correct parameters
        args = mock_update_food_entry.call_args[0]
        kwargs = mock_update_food_entry.call_args[1]
        assert args[0] == mock_db
        assert args[1] == 1  # entry_id
        assert kwargs['food'] == "Updated Apple"
        assert kwargs['calories'] == 100
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.update_food_entry')
    def test_update_food_command_not_found(self, mock_update_food_entry, mock_get_db):
        """Test the update-food command when entry is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock entry not found
        mock_update_food_entry.return_value = None
        
        # Run command
        result = self.runner.invoke(app, ["update-food", "999", "--food", "New Food"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Food entry not found" in result.stdout
        mock_update_food_entry.assert_called_once()
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.delete_food_entry')
    def test_delete_food_command(self, mock_delete_food_entry, mock_get_db):
        """Test the delete-food command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock successful deletion
        mock_delete_food_entry.return_value = True
        
        # Run command
        result = self.runner.invoke(app, ["delete-food", "1"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Food entry deleted" in result.stdout
        mock_delete_food_entry.assert_called_once_with(mock_db, 1)
    
    @patch('myapp.cli.food.get_db')
    @patch('myapp.cli.food.delete_food_entry')
    def test_delete_food_command_not_found(self, mock_delete_food_entry, mock_get_db):
        """Test the delete-food command when entry is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock failed deletion
        mock_delete_food_entry.return_value = False
        
        # Run command
        result = self.runner.invoke(app, ["delete-food", "999"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Food entry not found" in result.stdout
        mock_delete_food_entry.assert_called_once_with(mock_db, 999)
