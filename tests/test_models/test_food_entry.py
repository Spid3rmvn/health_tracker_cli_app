"""
Tests for the FoodEntry model.
"""
import pytest
from myapp.models.food_entry import FoodEntry
from datetime import date, timedelta


@pytest.mark.unit
class TestFoodEntryModel:
    """Test cases for the FoodEntry model."""
    
    def test_create_food_entry(self, test_db, sample_user):
        """Test creating a new food entry."""
        entry_date = date.today()
        food_entry = FoodEntry(
            user_id=sample_user.id,
            food="Banana",
            calories=105,
            date=entry_date
        )
        test_db.add(food_entry)
        test_db.commit()
        test_db.refresh(food_entry)
        
        assert food_entry.id is not None
        assert food_entry.user_id == sample_user.id
        assert food_entry.food == "Banana"
        assert food_entry.calories == 105
        assert food_entry.date == entry_date
    
    def test_food_entry_required_fields(self, test_db, sample_user):
        """Test that all required fields are enforced."""
        # Test missing food
        with pytest.raises(Exception):
            food_entry = FoodEntry(
                user_id=sample_user.id,
                calories=100,
                date=date.today()
            )
            test_db.add(food_entry)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing calories
        with pytest.raises(Exception):
            food_entry = FoodEntry(
                user_id=sample_user.id,
                food="Apple",
                date=date.today()
            )
            test_db.add(food_entry)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing date
        with pytest.raises(Exception):
            food_entry = FoodEntry(
                user_id=sample_user.id,
                food="Apple",
                calories=100
            )
            test_db.add(food_entry)
            test_db.commit()
        
        test_db.rollback()
        
        # Test missing user_id
        with pytest.raises(Exception):
            food_entry = FoodEntry(
                food="Apple",
                calories=100,
                date=date.today()
            )
            test_db.add(food_entry)
            test_db.commit()
    
    def test_food_entry_user_relationship(self, test_db, sample_user):
        """Test the relationship between food entry and user."""
        food_entry = FoodEntry(
            user_id=sample_user.id,
            food="Orange",
            calories=62,
            date=date.today()
        )
        test_db.add(food_entry)
        test_db.commit()
        test_db.refresh(food_entry)
        
        # Test the relationship
        assert food_entry.user is not None
        assert food_entry.user.id == sample_user.id
        assert food_entry.user.name == sample_user.name
    
    def test_multiple_food_entries_same_user(self, test_db, sample_user):
        """Test that a user can have multiple food entries."""
        entries = []
        foods = [("Apple", 95), ("Banana", 105), ("Orange", 62)]
        
        for food, calories in foods:
            entry = FoodEntry(
                user_id=sample_user.id,
                food=food,
                calories=calories,
                date=date.today()
            )
            entries.append(entry)
            test_db.add(entry)
        
        test_db.commit()
        
        # Refresh user to get updated relationships
        test_db.refresh(sample_user)
        
        assert len(sample_user.entries) == 3
        entry_foods = [entry.food for entry in sample_user.entries]
        assert "Apple" in entry_foods
        assert "Banana" in entry_foods
        assert "Orange" in entry_foods
    
    def test_food_entry_different_dates(self, test_db, sample_user):
        """Test food entries with different dates."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        entries = [
            FoodEntry(user_id=sample_user.id, food="Breakfast", calories=300, date=yesterday),
            FoodEntry(user_id=sample_user.id, food="Lunch", calories=500, date=today),
            FoodEntry(user_id=sample_user.id, food="Dinner", calories=700, date=tomorrow)
        ]
        
        for entry in entries:
            test_db.add(entry)
        test_db.commit()
        
        # Query entries by date
        today_entries = test_db.query(FoodEntry).filter(
            FoodEntry.user_id == sample_user.id,
            FoodEntry.date == today
        ).all()
        
        assert len(today_entries) == 1
        assert today_entries[0].food == "Lunch"
