"""
Tests for the User model.
"""
import pytest
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan
from datetime import date


@pytest.mark.unit
class TestUserModel:
    """Test cases for the User model."""
    
    def test_create_user(self, test_db):
        """Test creating a new user."""
        user = User(name="john_doe")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.name == "john_doe"
    
    def test_user_name_required(self, test_db):
        """Test that user name is required."""
        user = User()
        test_db.add(user)
        
        with pytest.raises(Exception):  # SQLAlchemy will raise an exception
            test_db.commit()
    
    def test_user_name_unique(self, test_db):
        """Test that user names must be unique."""
        user1 = User(name="duplicate_name")
        user2 = User(name="duplicate_name")
        
        test_db.add(user1)
        test_db.commit()
        
        test_db.add(user2)
        with pytest.raises(Exception):  # SQLAlchemy will raise an exception
            test_db.commit()
    
    def test_user_relationships(self, test_db, sample_user):
        """Test user relationships with other models."""
        # Add a food entry
        food_entry = FoodEntry(
            user_id=sample_user.id,
            food="Apple",
            calories=95,
            date=date.today()
        )
        test_db.add(food_entry)
        
        # Add a goal
        goal = Goal(
            user_id=sample_user.id,
            daily=2000,
            weekly=14000
        )
        test_db.add(goal)
        
        # Add a meal plan
        meal_plan = MealPlan(
            user_id=sample_user.id,
            week=1,
            plan="Healthy meals"
        )
        test_db.add(meal_plan)
        
        test_db.commit()
        test_db.refresh(sample_user)
        
        # Test relationships
        assert len(sample_user.entries) == 1
        assert len(sample_user.goals) == 1
        assert len(sample_user.meal_plans) == 1
        assert sample_user.entries[0].food == "Apple"
        assert sample_user.goals[0].daily == 2000
        assert sample_user.meal_plans[0].week == 1
    
    def test_user_cascade_delete(self, test_db, sample_user):
        """Test that deleting a user cascades to related records."""
        # Add related records
        food_entry = FoodEntry(
            user_id=sample_user.id,
            food="Apple",
            calories=95,
            date=date.today()
        )
        goal = Goal(
            user_id=sample_user.id,
            daily=2000,
            weekly=14000
        )
        meal_plan = MealPlan(
            user_id=sample_user.id,
            week=1,
            plan="Healthy meals"
        )
        
        test_db.add_all([food_entry, goal, meal_plan])
        test_db.commit()
        
        # Delete the user
        test_db.delete(sample_user)
        test_db.commit()
        
        # Verify related records are deleted
        assert test_db.query(FoodEntry).filter(FoodEntry.user_id == sample_user.id).count() == 0
        assert test_db.query(Goal).filter(Goal.user_id == sample_user.id).count() == 0
        assert test_db.query(MealPlan).filter(MealPlan.user_id == sample_user.id).count() == 0
