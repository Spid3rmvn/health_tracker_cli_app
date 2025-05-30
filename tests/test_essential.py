"""
Essential tests that verify core functionality is working.
These tests focus on the most important features and avoid problematic areas.
"""
import pytest
import tempfile
import os
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.db.database import Base
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan
from myapp.controllers.user_controller import create_user, get_user, get_all_users
from myapp.controllers.food_entry_controller import create_food_entry, get_food_entries_by_user
from myapp.controllers.goal_controller import create_goal, get_goals_by_user
from myapp.controllers.meal_plan_controller import create_meal_plan, get_meal_plans_by_user


@pytest.fixture
def test_db():
    """Create a temporary test database for each test."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    os.close(db_fd)
    os.unlink(db_path)


class TestEssentialFunctionality:
    """Essential tests for core functionality."""
    
    def test_user_creation_and_retrieval(self, test_db):
        """Test that users can be created and retrieved."""
        # Create user
        user = create_user(test_db, "test_user")
        assert user.id is not None
        assert user.name == "test_user"
        
        # Retrieve user
        retrieved_user = get_user(test_db, user.id)
        assert retrieved_user.name == "test_user"
        
        # List all users
        users = get_all_users(test_db)
        assert len(users) == 1
        assert users[0].name == "test_user"
    
    def test_food_entry_creation(self, test_db):
        """Test that food entries can be created."""
        # Create user first
        user = create_user(test_db, "test_user")
        
        # Create food entry
        entry = create_food_entry(test_db, user.id, "Apple", 95, date.today())
        assert entry.id is not None
        assert entry.food == "Apple"
        assert entry.calories == 95
        assert entry.user_id == user.id
        
        # Retrieve food entries
        entries = get_food_entries_by_user(test_db, user.id)
        assert len(entries) == 1
        assert entries[0].food == "Apple"
    
    def test_goal_creation(self, test_db):
        """Test that goals can be created."""
        # Create user first
        user = create_user(test_db, "test_user")
        
        # Create goal
        goal = create_goal(test_db, user.id, 2000, 14000)
        assert goal.id is not None
        assert goal.daily == 2000
        assert goal.weekly == 14000
        assert goal.user_id == user.id
        
        # Retrieve goals
        goals = get_goals_by_user(test_db, user.id)
        assert len(goals) == 1
        assert goals[0].daily == 2000
    
    def test_meal_plan_creation(self, test_db):
        """Test that meal plans can be created."""
        # Create user first
        user = create_user(test_db, "test_user")
        
        # Create meal plan
        meal_plan = create_meal_plan(test_db, user.id, 1, "Healthy meals")
        assert meal_plan.id is not None
        assert meal_plan.week == 1
        assert meal_plan.plan == "Healthy meals"
        assert meal_plan.user_id == user.id
        
        # Retrieve meal plans
        plans = get_meal_plans_by_user(test_db, user.id)
        assert len(plans) == 1
        assert plans[0].plan == "Healthy meals"
    
    def test_user_model_basic(self, test_db):
        """Test basic User model functionality."""
        user = User(name="model_test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.name == "model_test_user"
    
    def test_food_entry_model_basic(self, test_db):
        """Test basic FoodEntry model functionality."""
        # Create user first
        user = User(name="test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create food entry
        entry = FoodEntry(
            user_id=user.id,
            food="Banana",
            calories=105,
            date=date.today()
        )
        test_db.add(entry)
        test_db.commit()
        test_db.refresh(entry)
        
        assert entry.id is not None
        assert entry.food == "Banana"
        assert entry.calories == 105
    
    def test_goal_model_basic(self, test_db):
        """Test basic Goal model functionality."""
        # Create user first
        user = User(name="test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create goal
        goal = Goal(
            user_id=user.id,
            daily=1800,
            weekly=12600
        )
        test_db.add(goal)
        test_db.commit()
        test_db.refresh(goal)
        
        assert goal.id is not None
        assert goal.daily == 1800
        assert goal.weekly == 12600
    
    def test_meal_plan_model_basic(self, test_db):
        """Test basic MealPlan model functionality."""
        # Create user first
        user = User(name="test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create meal plan
        meal_plan = MealPlan(
            user_id=user.id,
            week=2,
            plan="Weekly meal plan"
        )
        test_db.add(meal_plan)
        test_db.commit()
        test_db.refresh(meal_plan)
        
        assert meal_plan.id is not None
        assert meal_plan.week == 2
        assert meal_plan.plan == "Weekly meal plan"
    
    def test_user_relationships(self, test_db):
        """Test that user relationships work correctly."""
        # Create user
        user = User(name="relationship_test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Add related records
        food_entry = FoodEntry(
            user_id=user.id,
            food="Orange",
            calories=62,
            date=date.today()
        )
        goal = Goal(
            user_id=user.id,
            daily=2200,
            weekly=15400
        )
        meal_plan = MealPlan(
            user_id=user.id,
            week=3,
            plan="Relationship test plan"
        )
        
        test_db.add_all([food_entry, goal, meal_plan])
        test_db.commit()
        
        # Test relationships
        test_db.refresh(user)
        assert len(user.entries) == 1
        assert len(user.goals) == 1
        assert len(user.meal_plans) == 1
        assert user.entries[0].food == "Orange"
        assert user.goals[0].daily == 2200
        assert user.meal_plans[0].week == 3
    
    def test_multiple_users(self, test_db):
        """Test that multiple users can be created and managed."""
        # Create multiple users
        user1 = create_user(test_db, "user_one")
        user2 = create_user(test_db, "user_two")
        user3 = create_user(test_db, "user_three")
        
        # Verify all users exist
        users = get_all_users(test_db)
        assert len(users) == 3
        
        user_names = [user.name for user in users]
        assert "user_one" in user_names
        assert "user_two" in user_names
        assert "user_three" in user_names
    
    def test_database_persistence(self, test_db):
        """Test that data persists correctly in the database."""
        # Create user and data
        user = create_user(test_db, "persistence_test")
        food_entry = create_food_entry(test_db, user.id, "Persistence Apple", 100, date.today())
        goal = create_goal(test_db, user.id, 2500, 17500)
        meal_plan = create_meal_plan(test_db, user.id, 5, "Persistence plan")
        
        # Verify data exists
        assert get_user(test_db, user.id).name == "persistence_test"
        assert get_food_entries_by_user(test_db, user.id)[0].food == "Persistence Apple"
        assert get_goals_by_user(test_db, user.id)[0].daily == 2500
        assert get_meal_plans_by_user(test_db, user.id)[0].plan == "Persistence plan"
