# Health Tracker CLI App - Test Suite

This directory contains comprehensive tests for the Health Tracker CLI application.

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── test_models/             # Model tests
│   ├── test_user.py         # User model tests
│   ├── test_food_entry.py   # FoodEntry model tests
│   ├── test_goal.py         # Goal model tests
│   └── test_meal_plan.py    # MealPlan model tests
├── test_controllers/        # Controller tests
│   ├── test_user_controller.py
│   ├── test_food_entry_controller.py
│   ├── test_goal_controller.py
│   ├── test_meal_plan_controller.py
│   └── test_report_controller.py
├── test_cli/               # CLI command tests
│   ├── test_main_cli.py    # Main CLI app tests
│   ├── test_user_cli.py    # User CLI commands
│   └── test_food_cli.py    # Food CLI commands
└── test_database/          # Database tests
    └── test_database.py    # Database functionality tests
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Test individual model classes
- Test model validation and constraints
- Test model relationships

### Integration Tests (`@pytest.mark.integration`)
- Test controller functions with database
- Test database operations
- Test data persistence and retrieval

### CLI Tests (`@pytest.mark.cli`)
- Test CLI command functionality
- Test command-line argument parsing
- Test CLI output and error handling

## Running Tests

### Prerequisites
Make sure you have the development dependencies installed:
```bash
poetry install
```

### Run All Tests
```bash
pytest tests/
```

### Run Tests with Verbose Output
```bash
pytest tests/ -v
```

### Run Tests with Coverage
```bash
pytest tests/ --cov=myapp --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/ -m unit

# Integration tests only
pytest tests/ -m integration

# CLI tests only
pytest tests/ -m cli
```

### Run Specific Test Files
```bash
# Model tests
pytest tests/test_models/

# Controller tests
pytest tests/test_controllers/

# CLI tests
pytest tests/test_cli/

# Database tests
pytest tests/test_database/
```

### Run Specific Test Classes or Functions
```bash
# Run a specific test class
pytest tests/test_models/test_user.py::TestUserModel

# Run a specific test function
pytest tests/test_models/test_user.py::TestUserModel::test_create_user
```

## Test Configuration

### Pytest Configuration
The test configuration is defined in `pytest.ini` and includes:
- Test discovery patterns
- Coverage settings
- Custom markers
- Output formatting

### Test Fixtures
Common test fixtures are defined in `conftest.py`:
- `test_db`: Temporary test database for each test
- `sample_user`: Pre-created user for testing
- `sample_food_entry`: Pre-created food entry for testing
- `sample_goal`: Pre-created goal for testing
- `sample_meal_plan`: Pre-created meal plan for testing
- `multiple_users`: Multiple users for testing
- `multiple_food_entries`: Multiple food entries for testing

## Test Database

Tests use a temporary SQLite database that is:
- Created fresh for each test function
- Automatically cleaned up after each test
- Isolated from the main application database
- Pre-populated with test data via fixtures

## Mocking

CLI tests use mocking to:
- Isolate CLI logic from database operations
- Test command-line interfaces without side effects
- Verify that correct controller functions are called
- Test error handling and edge cases

## Coverage

The test suite aims for high code coverage across:
- Model classes and their methods
- Controller functions
- CLI command handlers
- Database operations
- Error handling paths

## Adding New Tests

When adding new functionality:

1. **Model Tests**: Add tests in `test_models/` for new model classes
2. **Controller Tests**: Add tests in `test_controllers/` for new controller functions
3. **CLI Tests**: Add tests in `test_cli/` for new CLI commands
4. **Integration Tests**: Add tests that verify end-to-end functionality

### Test Naming Convention
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Test Documentation
Each test should have a clear docstring explaining:
- What functionality is being tested
- What the expected behavior is
- Any special setup or conditions

## Continuous Integration

These tests are designed to run in CI/CD environments and provide:
- Fast feedback on code changes
- Regression detection
- Code quality assurance
- Coverage reporting

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure the project is installed in development mode
2. **Database Errors**: Check that SQLAlchemy models are properly imported
3. **CLI Test Failures**: Verify that Typer commands are correctly mocked
4. **Coverage Issues**: Ensure all source files are included in coverage configuration

### Debug Mode
Run tests with more verbose output:
```bash
pytest tests/ -v -s --tb=long
```

### Test a Single Failing Test
```bash
pytest tests/path/to/test.py::test_function_name -v -s
```
