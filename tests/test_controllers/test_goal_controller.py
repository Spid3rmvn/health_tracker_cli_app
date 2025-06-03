"""
Tests for the goal controller functions.
"""
import pytest
from myapp.controllers.goal_controller import (
    create_goal, get_goal, get_goals_by_user, update_goal, delete_goal
)
from myapp.models.goal import Goal


@pytest.mark.integration
class TestGoalController:
    """Test cases for goal controller functions."""
    
    def test_create_goal(self, test_db, sample_user):
        """Test creating a goal through the controller."""
        goal = create_goal(test_db, sample_user.id, 2000, 14000)
        
        assert goal is not None
        assert goal.id is not None
        assert goal.user_id == sample_user.id
        assert goal.daily == 2000
        assert goal.weekly == 14000
        
        # Verify it's in the database
        db_goal = test_db.query(Goal).filter(Goal.id == goal.id).first()
        assert db_goal is not None
        assert db_goal.daily == 2000
        assert db_goal.weekly == 14000
    
    def test_get_goal(self, test_db, sample_goal):
        """Test getting a goal by ID."""
        goal = get_goal(test_db, sample_goal.id)
        
        assert goal is not None
        assert goal.id == sample_goal.id
        assert goal.daily == sample_goal.daily
        assert goal.weekly == sample_goal.weekly
    
    def test_get_goal_not_found(self, test_db):
        """Test getting a goal that doesn't exist."""
        goal = get_goal(test_db, 99999)
        assert goal is None
    
    def test_get_goals_by_user(self, test_db, sample_user):
        """Test getting all goals for a user."""
        # Create multiple goals
        goal1 = create_goal(test_db, sample_user.id, 2000, 14000)
        goal2 = create_goal(test_db, sample_user.id, 2200, 15400)
        goal3 = create_goal(test_db, sample_user.id, 1800, 12600)
        
        goals = get_goals_by_user(test_db, sample_user.id)
        
        assert len(goals) == 3
        daily_goals = [goal.daily for goal in goals]
        assert 2000 in daily_goals
        assert 2200 in daily_goals
        assert 1800 in daily_goals
    
    def test_get_goals_by_user_empty(self, test_db, sample_user):
        """Test getting goals for a user with no goals."""
        goals = get_goals_by_user(test_db, sample_user.id)
        assert goals == []
    
    def test_get_goals_by_nonexistent_user(self, test_db):
        """Test getting goals for a user that doesn't exist."""
        goals = get_goals_by_user(test_db, 99999)
        assert goals == []
    
    def test_update_goal_all_fields(self, test_db, sample_goal):
        """Test updating all fields of a goal."""
        updated_goal = update_goal(test_db, sample_goal.id, 2500, 17500)
        
        assert updated_goal is not None
        assert updated_goal.id == sample_goal.id
        assert updated_goal.daily == 2500
        assert updated_goal.weekly == 17500
        
        # Verify in database
        db_goal = test_db.query(Goal).filter(Goal.id == sample_goal.id).first()
        assert db_goal.daily == 2500
        assert db_goal.weekly == 17500
    
    def test_update_goal_partial(self, test_db, sample_goal):
        """Test updating only some fields of a goal."""
        original_weekly = sample_goal.weekly
        
        updated_goal = update_goal(test_db, sample_goal.id, daily=2500)
        
        assert updated_goal is not None
        assert updated_goal.daily == 2500
        assert updated_goal.weekly == original_weekly  # Unchanged
    
    def test_update_goal_not_found(self, test_db):
        """Test updating a goal that doesn't exist."""
        updated_goal = update_goal(test_db, 99999, 2000, 14000)
        assert updated_goal is None
    
    def test_update_goal_no_changes(self, test_db, sample_goal):
        """Test updating a goal with no changes."""
        original_daily = sample_goal.daily
        original_weekly = sample_goal.weekly
        
        updated_goal = update_goal(test_db, sample_goal.id)
        
        assert updated_goal is not None
        assert updated_goal.daily == original_daily
        assert updated_goal.weekly == original_weekly
    
    def test_delete_goal(self, test_db, sample_goal):
        """Test deleting a goal."""
        goal_id = sample_goal.id
        success = delete_goal(test_db, goal_id)
        
        assert success is True
        
        # Verify goal is deleted
        db_goal = test_db.query(Goal).filter(Goal.id == goal_id).first()
        assert db_goal is None
    
    def test_delete_goal_not_found(self, test_db):
        """Test deleting a goal that doesn't exist."""
        success = delete_goal(test_db, 99999)
        assert success is False
    
    def test_create_goal_zero_values(self, test_db, sample_user):
        """Test creating a goal with zero values."""
        goal = create_goal(test_db, sample_user.id, 0, 0)
        
        assert goal is not None
        assert goal.daily == 0
        assert goal.weekly == 0
