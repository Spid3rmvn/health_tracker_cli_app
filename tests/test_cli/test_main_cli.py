"""
Tests for the main CLI application.
"""
import pytest
from typer.testing import CliRunner
from myapp.cli.__main__ import app


@pytest.mark.cli
class TestMainCLI:
    """Test cases for the main CLI application."""
    
    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()
    
    def test_main_app_help(self):
        """Test that the main app shows help."""
        result = self.runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "Commands:" in result.stdout
    
    def test_user_subcommand_available(self):
        """Test that the user subcommand is available."""
        result = self.runner.invoke(app, ["user", "--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "user" in result.stdout.lower()
    
    def test_food_subcommand_available(self):
        """Test that the food subcommand is available."""
        result = self.runner.invoke(app, ["food", "--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "food" in result.stdout.lower()
    
    def test_goal_subcommand_available(self):
        """Test that the goal subcommand is available."""
        result = self.runner.invoke(app, ["goal", "--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "goal" in result.stdout.lower()
    
    def test_meal_plan_subcommand_available(self):
        """Test that the meal-plan subcommand is available."""
        result = self.runner.invoke(app, ["meal-plan", "--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
    
    def test_report_subcommand_available(self):
        """Test that the report subcommand is available."""
        result = self.runner.invoke(app, ["report", "--help"])
        
        assert result.exit_code == 0
        assert "Usage:" in result.stdout
        assert "report" in result.stdout.lower()
    
    def test_invalid_command(self):
        """Test behavior with invalid command."""
        result = self.runner.invoke(app, ["invalid-command"])
        
        assert result.exit_code != 0
        assert "No such command" in result.stdout or "Usage:" in result.stdout
    
    def test_app_structure(self):
        """Test that all expected subcommands are registered."""
        # Get help output to see available commands
        result = self.runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        output = result.stdout.lower()
        
        # Check that all expected subcommands are listed
        assert "user" in output
        assert "food" in output
        assert "goal" in output
        assert "meal-plan" in output
        assert "report" in output
