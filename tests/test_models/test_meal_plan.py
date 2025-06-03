"""
Tests for the MealPlan model.
"""
import pytest
from myapp.models.meal_plan import MealPlan


@pytest.mark.unit
class TestMealPlanModel:
    """Test cases for the MealPlan model."""
    
    def test_create_meal_plan(self, test_db, sample_user):
        """Test creating a new meal plan."""
        meal_plan = MealPlan(
            user_id=sample_user.id,
            week=2,
            plan="Breakfast: Oats, Lunch: Salad, Dinner: Fish"
        )
        test_db.add(meal_plan)
        test_db.commit()
        test_db.refresh(meal_plan)
        
        assert meal_plan.id is not None
        assert meal_plan.user_id == sample_user.id
        assert meal_plan.week == 2
        assert meal_plan.plan == "Breakfast: Oats, Lunch: Salad, Dinner: Fish"
    
    def test_meal_plan_required_fields(self, test_db, sample_user):
        """Test that all required fields are enforced."""
        # Test missing week
        with pytest.raises(Exception):
            meal_plan = MealPlan(
                user_id=sample_user.id,
                plan="Some plan"
            )
            test_db.add(meal_plan)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing plan
        with pytest.raises(Exception):
            meal_plan = MealPlan(
                user_id=sample_user.id,
                week=1
            )
            test_db.add(meal_plan)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing user_id
        with pytest.raises(Exception):
            meal_plan = MealPlan(
                week=1,
                plan="Some plan"
            )
            test_db.add(meal_plan)
            test_db.commit()
    
    def test_meal_plan_user_relationship(self, test_db, sample_user):
        """Test the relationship between meal plan and user."""
        meal_plan = MealPlan(
            user_id=sample_user.id,
            week=3,
            plan="Healthy weekly plan"
        )
        test_db.add(meal_plan)
        test_db.commit()
        test_db.refresh(meal_plan)
        
        # Test the relationship
        assert meal_plan.user is not None
        assert meal_plan.user.id == sample_user.id
        assert meal_plan.user.name == sample_user.name
    
    def test_multiple_meal_plans_same_user(self, test_db, sample_user):
        """Test that a user can have multiple meal plans."""
        meal_plans = [
            MealPlan(user_id=sample_user.id, week=1, plan="Week 1 plan"),
            MealPlan(user_id=sample_user.id, week=2, plan="Week 2 plan"),
            MealPlan(user_id=sample_user.id, week=3, plan="Week 3 plan")
        ]
        
        for plan in meal_plans:
            test_db.add(plan)
        test_db.commit()
        
        # Refresh user to get updated relationships
        test_db.refresh(sample_user)
        
        assert len(sample_user.meal_plans) == 3
        weeks = [plan.week for plan in sample_user.meal_plans]
        assert 1 in weeks
        assert 2 in weeks
        assert 3 in weeks
    
    def test_meal_plan_long_text(self, test_db, sample_user):
        """Test meal plan with long text content."""
        long_plan = """
        Monday: Breakfast - Oatmeal with berries, Lunch - Grilled chicken salad, Dinner - Salmon with vegetables
        Tuesday: Breakfast - Greek yogurt with granola, Lunch - Turkey sandwich, Dinner - Pasta with marinara
        Wednesday: Breakfast - Smoothie bowl, Lunch - Quinoa salad, Dinner - Stir-fry with tofu
        Thursday: Breakfast - Eggs and toast, Lunch - Soup and salad, Dinner - Grilled fish with rice
        Friday: Breakfast - Pancakes, Lunch - Wrap with vegetables, Dinner - Pizza night
        Saturday: Breakfast - French toast, Lunch - Burger and fries, Dinner - BBQ chicken
        Sunday: Breakfast - Brunch special, Lunch - Leftover night, Dinner - Family dinner
        """
        
        meal_plan = MealPlan(
            user_id=sample_user.id,
            week=4,
            plan=long_plan.strip()
        )
        test_db.add(meal_plan)
        test_db.commit()
        test_db.refresh(meal_plan)
        
        assert meal_plan.plan == long_plan.strip()
        assert len(meal_plan.plan) > 500  # Verify it's actually long
    
    def test_meal_plan_week_numbers(self, test_db, sample_user):
        """Test different week number values."""
        # Test various week numbers
        week_numbers = [1, 52, 0, -1, 100]
        
        for week_num in week_numbers:
            meal_plan = MealPlan(
                user_id=sample_user.id,
                week=week_num,
                plan=f"Plan for week {week_num}"
            )
            test_db.add(meal_plan)
        
        test_db.commit()
        
        # Verify all were created
        plans = test_db.query(MealPlan).filter(MealPlan.user_id == sample_user.id).all()
        assert len(plans) == len(week_numbers)
        
        stored_weeks = [plan.week for plan in plans]
        for week_num in week_numbers:
            assert week_num in stored_weeks
