"""
Tests for the food entry controller functions.
"""
import pytest
from datetime import date, timedelta
from myapp.controllers.food_entry_controller import (
    create_food_entry, get_food_entry, get_food_entries_by_user,
    update_food_entry, delete_food_entry
)
from myapp.models.food_entry import FoodEntry


@pytest.mark.integration
class TestFoodEntryController:
    """Test cases for food entry controller functions."""
    
    def test_create_food_entry(self, test_db, sample_user):
        """Test creating a food entry through the controller."""
        entry_date = date.today()
        entry = create_food_entry(test_db, sample_user.id, "Apple", 95, entry_date)
        
        assert entry is not None
        assert entry.id is not None
        assert entry.user_id == sample_user.id
        assert entry.food == "Apple"
        assert entry.calories == 95
        assert entry.date == entry_date
        
        # Verify it's in the database
        db_entry = test_db.query(FoodEntry).filter(FoodEntry.id == entry.id).first()
        assert db_entry is not None
        assert db_entry.food == "Apple"
    
    def test_get_food_entry(self, test_db, sample_food_entry):
        """Test getting a food entry by ID."""
        entry = get_food_entry(test_db, sample_food_entry.id)
        
        assert entry is not None
        assert entry.id == sample_food_entry.id
        assert entry.food == sample_food_entry.food
        assert entry.calories == sample_food_entry.calories
    
    def test_get_food_entry_not_found(self, test_db):
        """Test getting a food entry that doesn't exist."""
        entry = get_food_entry(test_db, 99999)
        assert entry is None
    
    def test_get_food_entries_by_user(self, test_db, multiple_food_entries, sample_user):
        """Test getting all food entries for a user."""
        entries = get_food_entries_by_user(test_db, sample_user.id)
        
        assert len(entries) == 3
        foods = [entry.food for entry in entries]
        assert "Apple" in foods
        assert "Banana" in foods
        assert "Orange" in foods
    
    def test_get_food_entries_by_user_empty(self, test_db, sample_user):
        """Test getting food entries for a user with no entries."""
        entries = get_food_entries_by_user(test_db, sample_user.id)
        assert entries == []
    
    def test_get_food_entries_by_nonexistent_user(self, test_db):
        """Test getting food entries for a user that doesn't exist."""
        entries = get_food_entries_by_user(test_db, 99999)
        assert entries == []
    
    def test_update_food_entry_all_fields(self, test_db, sample_food_entry):
        """Test updating all fields of a food entry."""
        new_date = date.today() + timedelta(days=1)
        updated_entry = update_food_entry(
            test_db, sample_food_entry.id, "Banana", 105, new_date
        )
        
        assert updated_entry is not None
        assert updated_entry.id == sample_food_entry.id
        assert updated_entry.food == "Banana"
        assert updated_entry.calories == 105
        assert updated_entry.date == new_date
        
        # Verify in database
        db_entry = test_db.query(FoodEntry).filter(FoodEntry.id == sample_food_entry.id).first()
        assert db_entry.food == "Banana"
        assert db_entry.calories == 105
        assert db_entry.date == new_date
    
    def test_update_food_entry_partial(self, test_db, sample_food_entry):
        """Test updating only some fields of a food entry."""
        original_calories = sample_food_entry.calories
        original_date = sample_food_entry.date
        
        updated_entry = update_food_entry(test_db, sample_food_entry.id, food="Orange")
        
        assert updated_entry is not None
        assert updated_entry.food == "Orange"
        assert updated_entry.calories == original_calories  # Unchanged
        assert updated_entry.date == original_date  # Unchanged
    
    def test_update_food_entry_not_found(self, test_db):
        """Test updating a food entry that doesn't exist."""
        updated_entry = update_food_entry(test_db, 99999, "Banana", 105)
        assert updated_entry is None
    
    def test_update_food_entry_no_changes(self, test_db, sample_food_entry):
        """Test updating a food entry with no changes."""
        original_food = sample_food_entry.food
        original_calories = sample_food_entry.calories
        original_date = sample_food_entry.date
        
        updated_entry = update_food_entry(test_db, sample_food_entry.id)
        
        assert updated_entry is not None
        assert updated_entry.food == original_food
        assert updated_entry.calories == original_calories
        assert updated_entry.date == original_date
    
    def test_delete_food_entry(self, test_db, sample_food_entry):
        """Test deleting a food entry."""
        entry_id = sample_food_entry.id
        success = delete_food_entry(test_db, entry_id)
        
        assert success is True
        
        # Verify entry is deleted
        db_entry = test_db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()
        assert db_entry is None
    
    def test_delete_food_entry_not_found(self, test_db):
        """Test deleting a food entry that doesn't exist."""
        success = delete_food_entry(test_db, 99999)
        assert success is False
