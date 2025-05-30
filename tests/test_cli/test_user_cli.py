"""
Tests for the user CLI commands.
"""
import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from myapp.cli.user import app
from myapp.models.user import User


@pytest.mark.cli
class TestUserCLI:
    """Test cases for user CLI commands."""
    
    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.create_user')
    def test_add_user_command(self, mock_create_user, mock_get_db):
        """Test the add-user command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user creation
        mock_user = User(id=1, name="test_user")
        mock_create_user.return_value = mock_user
        
        # Run command
        result = self.runner.invoke(app, ["add-user", "test_user"])
        
        # Assertions
        assert result.exit_code == 0
        assert "User created with ID 1 and name 'test_user'" in result.stdout
        mock_create_user.assert_called_once_with(mock_db, "test_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_user_by_name')
    def test_get_user_command_found(self, mock_get_user_by_name, mock_get_db):
        """Test the get-user command when user is found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user retrieval
        mock_user = User(id=1, name="test_user")
        mock_get_user_by_name.return_value = mock_user
        
        # Run command
        result = self.runner.invoke(app, ["get-user", "test_user"])
        
        # Assertions
        assert result.exit_code == 0
        assert "ID: 1, Name: test_user" in result.stdout
        mock_get_user_by_name.assert_called_once_with(mock_db, "test_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_user_by_name')
    def test_get_user_command_not_found(self, mock_get_user_by_name, mock_get_db):
        """Test the get-user command when user is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user not found
        mock_get_user_by_name.return_value = None
        
        # Run command
        result = self.runner.invoke(app, ["get-user", "nonexistent_user"])
        
        # Assertions
        assert result.exit_code == 0
        assert "User not found" in result.stdout
        mock_get_user_by_name.assert_called_once_with(mock_db, "nonexistent_user")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_all_users')
    def test_list_users_command(self, mock_get_all_users, mock_get_db):
        """Test the list-users command."""
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
        result = self.runner.invoke(app, ["list-users"])
        
        # Assertions
        assert result.exit_code == 0
        assert "ID: 1, Name: user1" in result.stdout
        assert "ID: 2, Name: user2" in result.stdout
        assert "ID: 3, Name: user3" in result.stdout
        mock_get_all_users.assert_called_once_with(mock_db)
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.get_all_users')
    def test_list_users_command_empty(self, mock_get_all_users, mock_get_db):
        """Test the list-users command when no users exist."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock empty users list
        mock_get_all_users.return_value = []
        
        # Run command
        result = self.runner.invoke(app, ["list-users"])
        
        # Assertions
        assert result.exit_code == 0
        # Should not output any user information
        assert "ID:" not in result.stdout
        mock_get_all_users.assert_called_once_with(mock_db)
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.update_user')
    def test_update_user_command(self, mock_update_user, mock_get_db):
        """Test the update-user command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user update
        mock_user = User(id=1, name="updated_name")
        mock_update_user.return_value = mock_user
        
        # Run command
        result = self.runner.invoke(app, ["update-user", "1", "--name", "updated_name"])
        
        # Assertions
        assert result.exit_code == 0
        assert "Updated user ID 1" in result.stdout
        mock_update_user.assert_called_once_with(mock_db, 1, "updated_name")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.update_user')
    def test_update_user_command_not_found(self, mock_update_user, mock_get_db):
        """Test the update-user command when user is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock user not found
        mock_update_user.return_value = None
        
        # Run command
        result = self.runner.invoke(app, ["update-user", "999", "--name", "new_name"])
        
        # Assertions
        assert result.exit_code == 0
        assert "User not found" in result.stdout
        mock_update_user.assert_called_once_with(mock_db, 999, "new_name")
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.delete_user')
    def test_delete_user_command(self, mock_delete_user, mock_get_db):
        """Test the delete-user command."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock successful deletion
        mock_delete_user.return_value = True
        
        # Run command
        result = self.runner.invoke(app, ["delete-user", "1"])
        
        # Assertions
        assert result.exit_code == 0
        assert "User deleted" in result.stdout
        mock_delete_user.assert_called_once_with(mock_db, 1)
    
    @patch('myapp.cli.user.get_db')
    @patch('myapp.cli.user.delete_user')
    def test_delete_user_command_not_found(self, mock_delete_user, mock_get_db):
        """Test the delete-user command when user is not found."""
        # Mock database session
        mock_db = MagicMock()
        mock_get_db.return_value.__enter__.return_value = mock_db
        
        # Mock failed deletion
        mock_delete_user.return_value = False
        
        # Run command
        result = self.runner.invoke(app, ["delete-user", "999"])
        
        # Assertions
        assert result.exit_code == 0
        assert "User not found" in result.stdout
        mock_delete_user.assert_called_once_with(mock_db, 999)
