"""
Tests for the meal plan controller functions.
"""
import pytest
from myapp.controllers.meal_plan_controller import (
    create_meal_plan, get_meal_plan, get_meal_plans_by_user,
    update_meal_plan, delete_meal_plan
)
from myapp.models.meal_plan import MealPlan


@pytest.mark.integration
class TestMealPlanController:
    """Test cases for meal plan controller functions."""
    
    def test_create_meal_plan(self, test_db, sample_user):
        """Test creating a meal plan through the controller."""
        plan_text = "Breakfast: Oats, Lunch: Salad, Dinner: Fish"
        meal_plan = create_meal_plan(test_db, sample_user.id, 1, plan_text)
        
        assert meal_plan is not None
        assert meal_plan.id is not None
        assert meal_plan.user_id == sample_user.id
        assert meal_plan.week == 1
        assert meal_plan.plan == plan_text
        
        # Verify it's in the database
        db_plan = test_db.query(MealPlan).filter(MealPlan.id == meal_plan.id).first()
        assert db_plan is not None
        assert db_plan.plan == plan_text
    
    def test_get_meal_plan(self, test_db, sample_meal_plan):
        """Test getting a meal plan by ID."""
        meal_plan = get_meal_plan(test_db, sample_meal_plan.id)
        
        assert meal_plan is not None
        assert meal_plan.id == sample_meal_plan.id
        assert meal_plan.week == sample_meal_plan.week
        assert meal_plan.plan == sample_meal_plan.plan
    
    def test_get_meal_plan_not_found(self, test_db):
        """Test getting a meal plan that doesn't exist."""
        meal_plan = get_meal_plan(test_db, 99999)
        assert meal_plan is None
    
    def test_get_meal_plans_by_user(self, test_db, sample_user):
        """Test getting all meal plans for a user."""
        # Create multiple meal plans
        plan1 = create_meal_plan(test_db, sample_user.id, 1, "Week 1 plan")
        plan2 = create_meal_plan(test_db, sample_user.id, 2, "Week 2 plan")
        plan3 = create_meal_plan(test_db, sample_user.id, 3, "Week 3 plan")
        
        meal_plans = get_meal_plans_by_user(test_db, sample_user.id)
        
        assert len(meal_plans) == 3
        weeks = [plan.week for plan in meal_plans]
        assert 1 in weeks
        assert 2 in weeks
        assert 3 in weeks
    
    def test_get_meal_plans_by_user_empty(self, test_db, sample_user):
        """Test getting meal plans for a user with no plans."""
        meal_plans = get_meal_plans_by_user(test_db, sample_user.id)
        assert meal_plans == []
    
    def test_get_meal_plans_by_nonexistent_user(self, test_db):
        """Test getting meal plans for a user that doesn't exist."""
        meal_plans = get_meal_plans_by_user(test_db, 99999)
        assert meal_plans == []
    
    def test_update_meal_plan_all_fields(self, test_db, sample_meal_plan):
        """Test updating all fields of a meal plan."""
        new_plan = "Updated meal plan content"
        updated_plan = update_meal_plan(test_db, sample_meal_plan.id, 5, new_plan)
        
        assert updated_plan is not None
        assert updated_plan.id == sample_meal_plan.id
        assert updated_plan.week == 5
        assert updated_plan.plan == new_plan
        
        # Verify in database
        db_plan = test_db.query(MealPlan).filter(MealPlan.id == sample_meal_plan.id).first()
        assert db_plan.week == 5
        assert db_plan.plan == new_plan
    
    def test_update_meal_plan_partial(self, test_db, sample_meal_plan):
        """Test updating only some fields of a meal plan."""
        original_plan = sample_meal_plan.plan
        
        updated_plan = update_meal_plan(test_db, sample_meal_plan.id, week=10)
        
        assert updated_plan is not None
        assert updated_plan.week == 10
        assert updated_plan.plan == original_plan  # Unchanged
    
    def test_update_meal_plan_not_found(self, test_db):
        """Test updating a meal plan that doesn't exist."""
        updated_plan = update_meal_plan(test_db, 99999, 1, "New plan")
        assert updated_plan is None
    
    def test_update_meal_plan_no_changes(self, test_db, sample_meal_plan):
        """Test updating a meal plan with no changes."""
        original_week = sample_meal_plan.week
        original_plan = sample_meal_plan.plan
        
        updated_plan = update_meal_plan(test_db, sample_meal_plan.id)
        
        assert updated_plan is not None
        assert updated_plan.week == original_week
        assert updated_plan.plan == original_plan
    
    def test_delete_meal_plan(self, test_db, sample_meal_plan):
        """Test deleting a meal plan."""
        plan_id = sample_meal_plan.id
        success = delete_meal_plan(test_db, plan_id)
        
        assert success is True
        
        # Verify meal plan is deleted
        db_plan = test_db.query(MealPlan).filter(MealPlan.id == plan_id).first()
        assert db_plan is None
    
    def test_delete_meal_plan_not_found(self, test_db):
        """Test deleting a meal plan that doesn't exist."""
        success = delete_meal_plan(test_db, 99999)
        assert success is False
    
    def test_create_meal_plan_long_content(self, test_db, sample_user):
        """Test creating a meal plan with long content."""
        long_plan = "Very long meal plan content " * 100
        meal_plan = create_meal_plan(test_db, sample_user.id, 52, long_plan)
        
        assert meal_plan is not None
        assert meal_plan.plan == long_plan
        assert len(meal_plan.plan) > 1000
