"""
Tests for the Goal model.
"""
import pytest
from myapp.models.goal import Goal


@pytest.mark.unit
class TestGoalModel:
    """Test cases for the Goal model."""
    
    def test_create_goal(self, test_db, sample_user):
        """Test creating a new goal."""
        goal = Goal(
            user_id=sample_user.id,
            daily=2500,
            weekly=17500
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        assert goal.id is not None
        assert goal.user_id == sample_user.id
        assert goal.daily == 2500
        assert goal.weekly == 17500
    
    def test_goal_required_fields(self, test_db, sample_user):
        """Test that all required fields are enforced."""
        # Test missing daily
        with pytest.raises(Exception):
            goal = Goal(
                user_id=sample_user.id,
                weekly=14000
            )
            test_db.add(goal)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing weekly
        with pytest.raises(Exception):
            goal = Goal(
                user_id=sample_user.id,
                daily=2000
            )
            test_db.add(goal)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing user_id
        with pytest.raises(Exception):
            goal = Goal(
                daily=2000,
                weekly=14000
            )
            test_db.add(goal)
            test_db.commit()
    
    def test_goal_user_relationship(self, test_db, sample_user):
        """Test the relationship between goal and user."""
        goal = Goal(
            user_id=sample_user.id,
            daily=1800,
            weekly=12600
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        # Test the relationship
        assert goal.user is not None
        assert goal.user.id == sample_user.id
        assert goal.user.name == sample_user.name
    
    def test_multiple_goals_same_user(self, test_db, sample_user):
        """Test that a user can have multiple goals."""
        goals = [
            Goal(user_id=sample_user.id, daily=2000, weekly=14000),
            Goal(user_id=sample_user.id, daily=2200, weekly=15400),
            Goal(user_id=sample_user.id, daily=1800, weekly=12600)
        ]
        
        for goal in goals:
            test_db.add(goal)
        test_db.commit()
        
        # Refresh user to get updated relationships
        test_db.refresh(sample_user)
        
        assert len(sample_user.goals) == 3
        daily_goals = [goal.daily for goal in sample_user.goals]
        assert 2000 in daily_goals
        assert 2200 in daily_goals
        assert 1800 in daily_goals
    
    def test_goal_integer_values(self, test_db, sample_user):
        """Test that goal values are properly stored as integers."""
        goal = Goal(
            user_id=sample_user.id,
            daily=2000,
            weekly=14000
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        assert isinstance(goal.daily, int)
        assert isinstance(goal.weekly, int)
        assert goal.daily == 2000
        assert goal.weekly == 14000
    
    def test_goal_zero_values(self, test_db, sample_user):
        """Test that zero values are allowed for goals."""
        goal = Goal(
            user_id=sample_user.id,
            daily=0,
            weekly=0
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        assert goal.daily == 0
        assert goal.weekly == 0
    
    def test_goal_negative_values(self, test_db, sample_user):
        """Test behavior with negative values (should be allowed by model)."""
        goal = Goal(
            user_id=sample_user.id,
            daily=-100,
            weekly=-700
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        assert goal.daily == -100
        assert goal.weekly == -700
