"""
Tests for the report controller functions.
"""
import pytest
from datetime import date, timedelta
from myapp.controllers.report_controller import generate_user_report
from myapp.controllers.food_entry_controller import create_food_entry


@pytest.mark.integration
class TestReportController:
    """Test cases for report controller functions."""
    
    def test_generate_user_report_with_entries(self, test_db, sample_user):
        """Test generating a report for a user with food entries."""
        # Create food entries for different dates
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        create_food_entry(test_db, sample_user.id, "Apple", 95, yesterday)
        create_food_entry(test_db, sample_user.id, "Banana", 105, today)
        create_food_entry(test_db, sample_user.id, "Orange", 62, today)
        
        # Generate report for the date range
        report = generate_user_report(test_db, sample_user.id, yesterday, today)
        
        assert report is not None
        assert report["user_id"] == sample_user.id
        assert report["total_entries"] == 3
        assert report["total_calories"] == 262  # 95 + 105 + 62
        assert report["start_date"] == yesterday
        assert report["end_date"] == today
    
    def test_generate_user_report_no_entries(self, test_db, sample_user):
        """Test generating a report for a user with no food entries."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        report = generate_user_report(test_db, sample_user.id, yesterday, today)
        
        assert report is not None
        assert report["user_id"] == sample_user.id
        assert report["total_entries"] == 0
        assert report["total_calories"] == 0
        assert report["start_date"] == yesterday
        assert report["end_date"] == today
    
    def test_generate_user_report_partial_date_range(self, test_db, sample_user):
        """Test generating a report for a partial date range."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        
        # Create entries on different days
        create_food_entry(test_db, sample_user.id, "Breakfast", 300, two_days_ago)
        create_food_entry(test_db, sample_user.id, "Lunch", 500, yesterday)
        create_food_entry(test_db, sample_user.id, "Dinner", 700, today)
        
        # Generate report only for yesterday to today
        report = generate_user_report(test_db, sample_user.id, yesterday, today)
        
        assert report["total_entries"] == 2  # Only lunch and dinner
        assert report["total_calories"] == 1200  # 500 + 700
    
    def test_generate_user_report_single_day(self, test_db, sample_user):
        """Test generating a report for a single day."""
        today = date.today()
        
        create_food_entry(test_db, sample_user.id, "Breakfast", 300, today)
        create_food_entry(test_db, sample_user.id, "Lunch", 500, today)
        create_food_entry(test_db, sample_user.id, "Snack", 150, today)
        
        # Generate report for today only
        report = generate_user_report(test_db, sample_user.id, today, today)
        
        assert report["total_entries"] == 3
        assert report["total_calories"] == 950  # 300 + 500 + 150
        assert report["start_date"] == today
        assert report["end_date"] == today
    
    def test_generate_user_report_nonexistent_user(self, test_db):
        """Test generating a report for a user that doesn't exist."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        report = generate_user_report(test_db, 99999, yesterday, today)
        
        assert report is not None
        assert report["user_id"] == 99999
        assert report["total_entries"] == 0
        assert report["total_calories"] == 0
    
    def test_generate_user_report_future_dates(self, test_db, sample_user):
        """Test generating a report for future dates."""
        today = date.today()
        tomorrow = today + timedelta(days=1)
        day_after = today + timedelta(days=2)
        
        # Create entry for today
        create_food_entry(test_db, sample_user.id, "Apple", 95, today)
        
        # Generate report for future dates
        report = generate_user_report(test_db, sample_user.id, tomorrow, day_after)
        
        assert report["total_entries"] == 0
        assert report["total_calories"] == 0
    
    def test_generate_user_report_reverse_date_range(self, test_db, sample_user):
        """Test generating a report with end date before start date."""
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        create_food_entry(test_db, sample_user.id, "Apple", 95, yesterday)
        create_food_entry(test_db, sample_user.id, "Banana", 105, today)
        
        # Generate report with reversed dates (end before start)
        report = generate_user_report(test_db, sample_user.id, today, yesterday)
        
        # Should return no entries since the date range is invalid
        assert report["total_entries"] == 0
        assert report["total_calories"] == 0
