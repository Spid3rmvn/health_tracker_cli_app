"""
Tests for the user controller functions.
"""
import pytest
from myapp.controllers.user_controller import (
    create_user, get_user, get_user_by_name, get_all_users, update_user, delete_user
)
from myapp.models.user import User


@pytest.mark.integration
class TestUserController:
    """Test cases for user controller functions."""
    
    def test_create_user(self, test_db):
        """Test creating a user through the controller."""
        user = create_user(test_db, "john_doe")
        
        assert user is not None
        assert user.id is not None
        assert user.name == "john_doe"
        
        # Verify it's in the database
        db_user = test_db.query(User).filter(User.id == user.id).first()
        assert db_user is not None
        assert db_user.name == "john_doe"
    
    def test_get_user(self, test_db, sample_user):
        """Test getting a user by ID."""
        user = get_user(test_db, sample_user.id)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.name == sample_user.name
    
    def test_get_user_not_found(self, test_db):
        """Test getting a user that doesn't exist."""
        user = get_user(test_db, 99999)
        assert user is None
    
    def test_get_user_by_name(self, test_db, sample_user):
        """Test getting a user by name."""
        user = get_user_by_name(test_db, sample_user.name)
        
        assert user is not None
        assert user.id == sample_user.id
        assert user.name == sample_user.name
    
    def test_get_user_by_name_not_found(self, test_db):
        """Test getting a user by name that doesn't exist."""
        user = get_user_by_name(test_db, "nonexistent_user")
        assert user is None
    
    def test_get_all_users(self, test_db, multiple_users):
        """Test getting all users."""
        users = get_all_users(test_db)
        
        assert len(users) == 3
        user_names = [user.name for user in users]
        assert "user_0" in user_names
        assert "user_1" in user_names
        assert "user_2" in user_names
    
    def test_get_all_users_empty(self, test_db):
        """Test getting all users when none exist."""
        users = get_all_users(test_db)
        assert users == []
    
    def test_update_user(self, test_db, sample_user):
        """Test updating a user."""
        updated_user = update_user(test_db, sample_user.id, "new_name")
        
        assert updated_user is not None
        assert updated_user.id == sample_user.id
        assert updated_user.name == "new_name"
        
        # Verify in database
        db_user = test_db.query(User).filter(User.id == sample_user.id).first()
        assert db_user.name == "new_name"
    
    def test_update_user_not_found(self, test_db):
        """Test updating a user that doesn't exist."""
        updated_user = update_user(test_db, 99999, "new_name")
        assert updated_user is None
    
    def test_update_user_no_changes(self, test_db, sample_user):
        """Test updating a user with no changes."""
        original_name = sample_user.name
        updated_user = update_user(test_db, sample_user.id, None)
        
        assert updated_user is not None
        assert updated_user.name == original_name
    
    def test_delete_user(self, test_db, sample_user):
        """Test deleting a user."""
        user_id = sample_user.id
        success = delete_user(test_db, user_id)
        
        assert success is True
        
        # Verify user is deleted
        db_user = test_db.query(User).filter(User.id == user_id).first()
        assert db_user is None
    
    def test_delete_user_not_found(self, test_db):
        """Test deleting a user that doesn't exist."""
        success = delete_user(test_db, 99999)
        assert success is False
    
    def test_create_user_duplicate_name(self, test_db):
        """Test creating users with duplicate names."""
        create_user(test_db, "duplicate_name")
        
        # This should raise an exception due to unique constraint
        with pytest.raises(Exception):
            create_user(test_db, "duplicate_name")
