"""
Tests for database functionality.
"""
import pytest
import tempfile
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from myapp.db.database import Base
from myapp.db.db import get_db
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan


@pytest.mark.integration
class TestDatabase:
    """Test cases for database functionality."""

    def test_database_connection(self):
        """Test that we can create a database connection."""
        # Create a temporary database
        db_fd, db_path = tempfile.mkstemp(suffix='.db')

        try:
            # Create engine
            engine = create_engine(f"sqlite:///{db_path}", echo=False)

            # Create tables
            Base.metadata.create_all(bind=engine)

            # Create session
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session = SessionLocal()

            # Test connection by creating a simple query
            result = session.execute(text("SELECT 1")).fetchone()
            assert result is not None and result[0] == 1

            session.close()

        finally:
            # Cleanup
            os.close(db_fd)
            os.unlink(db_path)

    def test_table_creation(self):
        """Test that all tables are created correctly."""
        # Create a temporary database
        db_fd, db_path = tempfile.mkstemp(suffix='.db')

        try:
            # Create engine
            engine = create_engine(f"sqlite:///{db_path}", echo=False)

            # Create tables
            Base.metadata.create_all(bind=engine)

            # Check that tables exist
            from sqlalchemy import inspect
            inspector = inspect(engine)
            table_names = inspector.get_table_names()

            assert 'users' in table_names
            assert 'food_entries' in table_names
            assert 'goals' in table_names
            assert 'meal_plans' in table_names

        finally:
            # Cleanup
            os.close(db_fd)
            os.unlink(db_path)

    def test_table_relationships(self, test_db):
        """Test that table relationships work correctly."""
        # Create a user
        user = User(name="test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # Create related records
        food_entry = FoodEntry(
            user_id=user.id,
            food="Apple",
            calories=95,
            date="2024-01-01"
        )
        goal = Goal(
            user_id=user.id,
            daily=2000,
            weekly=14000
        )
        meal_plan = MealPlan(
            user_id=user.id,
            week=1,
            plan="Healthy meals"
        )

        test_db.add_all([food_entry, goal, meal_plan])
        test_db.commit()

        # Test relationships
        test_db.refresh(user)
        assert len(user.entries) == 1
        assert len(user.goals) == 1
        assert len(user.meal_plans) == 1

        # Test back references
        assert food_entry.user.name == "test_user"
        assert goal.user.name == "test_user"
        assert meal_plan.user.name == "test_user"

    def test_cascade_delete(self, test_db):
        """Test that cascade delete works correctly."""
        # Create a user with related records
        user = User(name="test_user")
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        # Create related records
        food_entry = FoodEntry(
            user_id=user.id,
            food="Apple",
            calories=95,
            date="2024-01-01"
        )
        goal = Goal(
            user_id=user.id,
            daily=2000,
            weekly=14000
        )
        meal_plan = MealPlan(
            user_id=user.id,
            week=1,
            plan="Healthy meals"
        )

        test_db.add_all([food_entry, goal, meal_plan])
        test_db.commit()

        # Delete the user
        test_db.delete(user)
        test_db.commit()

        # Verify related records are deleted
        assert test_db.query(FoodEntry).filter(FoodEntry.user_id == user.id).count() == 0
        assert test_db.query(Goal).filter(Goal.user_id == user.id).count() == 0
        assert test_db.query(MealPlan).filter(MealPlan.user_id == user.id).count() == 0

    def test_get_db_context_manager(self):
        """Test the get_db context manager."""
        with get_db() as db:
            # Test that we get a valid session
            assert db is not None

            # Test that we can execute a query
            result = db.execute(text("SELECT 1")).fetchone()
            assert result is not None and result[0] == 1

    def test_database_constraints(self, test_db):
        """Test database constraints."""
        # Test unique constraint on user name
        user1 = User(name="unique_name")
        user2 = User(name="unique_name")

        test_db.add(user1)
        test_db.commit()

        test_db.add(user2)
        with pytest.raises(Exception):  # Should raise integrity error
            test_db.commit()

        test_db.rollback()

        # Test foreign key constraint
        with pytest.raises(Exception):  # Should raise integrity error
            invalid_entry = FoodEntry(
                user_id=99999,  # Non-existent user
                food="Apple",
                calories=95,
                date="2024-01-01"
            )
            test_db.add(invalid_entry)
            test_db.commit()

    def test_database_transactions(self, test_db):
        """Test database transaction handling."""
        # Start a transaction
        user = User(name="transaction_test")
        test_db.add(user)

        # Don't commit yet
        # Query in same session should see the user
        found_user = test_db.query(User).filter(User.name == "transaction_test").first()
        assert found_user is not None

        # Rollback the transaction
        test_db.rollback()

        # User should no longer exist
        found_user = test_db.query(User).filter(User.name == "transaction_test").first()
        assert found_user is None
