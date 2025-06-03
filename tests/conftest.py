"""
Pytest configuration and fixtures for the health tracker CLI app.
"""
import pytest
import tempfile
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from myapp.db.database import Base
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan
from datetime import date, datetime


@pytest.fixture(scope="function")
def test_db():
    """Create a temporary test database for each test."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    # Create engine with the temporary database
    engine = create_engine(f"sqlite:///{db_path}", echo=False)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    yield session

    # Cleanup
    session.close()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_user(test_db):
    """Create a sample user for testing."""
    user = User(name="test_user")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def sample_food_entry(test_db, sample_user):
    """Create a sample food entry for testing."""
    entry = FoodEntry(
        user_id=sample_user.id,
        food="Apple",
        calories=95,
        date=date.today()
    )
    test_db.add(entry)
    test_db.commit()
    test_db.refresh(entry)
    return entry


@pytest.fixture
def sample_goal(test_db, sample_user):
    """Create a sample goal for testing."""
    goal = Goal(
        user_id=sample_user.id,
        daily=2000,
        weekly=14000
    )
    test_db.add(goal)
    test_db.commit()
    test_db.refresh(goal)
    return goal


@pytest.fixture
def sample_meal_plan(test_db, sample_user):
    """Create a sample meal plan for testing."""
    meal_plan = MealPlan(
        user_id=sample_user.id,
        week=1,
        plan="Breakfast: Oatmeal, Lunch: Salad, Dinner: Chicken"
    )
    test_db.add(meal_plan)
    test_db.commit()
    test_db.refresh(meal_plan)
    return meal_plan


@pytest.fixture
def multiple_users(test_db):
    """Create multiple users for testing."""
    users = []
    for i in range(3):
        user = User(name=f"user_{i}")
        test_db.add(user)
        users.append(user)
    test_db.commit()
    for user in users:
        test_db.refresh(user)
    return users


@pytest.fixture
def multiple_food_entries(test_db, sample_user):
    """Create multiple food entries for testing."""
    entries = []
    foods = [("Apple", 95), ("Banana", 105), ("Orange", 62)]
    for i, (food, calories) in enumerate(foods):
        entry = FoodEntry(
            user_id=sample_user.id,
            food=food,
            calories=calories,
            date=date.today()
        )
        test_db.add(entry)
        entries.append(entry)
    test_db.commit()
    for entry in entries:
        test_db.refresh(entry)
    return entries
