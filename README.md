# 🏃‍♂️ Health Tracker CLI App

A comprehensive command-line application for tracking daily food intake, setting nutrition goals, and planning weekly meals. Built with Python, SQLAlchemy, and Typer for an intuitive CLI experience.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Development](#-development)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)

## ✨ Features

### 👤 User Management

- Create and manage user profiles
- Unique username validation
- User data persistence

### 🍎 Food Tracking

- Log daily food intake with calories
- Date-based food entry tracking
- Update and delete food entries
- View food history by user

### 🎯 Goal Setting

- Set daily and weekly calorie goals
- Track multiple goals per user
- Update and manage nutrition targets

### 📅 Meal Planning

- Create weekly meal plans
- Organize meals by week number
- Update and manage meal schedules

### 📊 Reporting

- Generate nutrition reports by date range
- View total calories and entries
- Track progress over time

## 🚀 Installation

### Prerequisites

- Python 3.12+
- Poetry (recommended) or pip

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd health_tracker_cli_app

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd health_tracker_cli_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
# Create database tables
python create_tables.py
```

## 🏁 Quick Start

### 1. Create a User

```bash
python -m myapp.cli user add-user "john_doe"
```

### 2. Add Food Entry

```bash
python -m myapp.cli food add-food 1 "Apple" 95 --date "2024-01-15"
```

### 3. Set Goals

```bash
python -m myapp.cli goal add-goal 1 2000 14000
```

### 4. Create Meal Plan

```bash
python -m myapp.cli meal-plan add-meal-plan 1 1 "Breakfast: Oats, Lunch: Salad, Dinner: Chicken"
```

### 5. Generate Report

```bash
python -m myapp.cli report user-report 1 "2024-01-01" "2024-01-31"
```

## 📖 Usage

The application provides five main command groups: `user`, `food`, `goal`, `meal-plan`, and `report`.

### 👤 User Commands

#### Create a User

```bash
python -m myapp.cli user add-user <name>
```

**Example:**

```bash
python -m myapp.cli user add-user "alice_smith"
```

#### Get User by Name

```bash
python -m myapp.cli user get-user <name>
```

**Example:**

```bash
python -m myapp.cli user get-user "alice_smith"
```

#### List All Users

```bash
python -m myapp.cli user list-users
```

#### Update User

```bash
python -m myapp.cli user update-user-cmd <user_id> --name <new_name>
```

**Example:**

```bash
python -m myapp.cli user update-user-cmd 1 --name "alice_johnson"
```

#### Delete User

```bash
python -m myapp.cli user delete-user-cmd <user_id>
```

**Example:**

```bash
python -m myapp.cli user delete-user-cmd 1
```

### 🍎 Food Commands

#### Add Food Entry

```bash
python -m myapp.cli food add-food <user_id> <food_name> <calories> [--date YYYY-MM-DD]
```

**Examples:**

```bash
# Add food for today
python -m myapp.cli food add-food 1 "Banana" 105

# Add food for specific date
python -m myapp.cli food add-food 1 "Apple" 95 --date "2024-01-15"
```

#### List Food Entries

```bash
python -m myapp.cli food list-food-entries <user_id>
```

**Example:**

```bash
python -m myapp.cli food list-food-entries 1
```

#### Update Food Entry

```bash
python -m myapp.cli food update-food-entry-cmd <entry_id> [--food <name>] [--calories <amount>] [--date YYYY-MM-DD]
```

**Example:**

```bash
python -m myapp.cli food update-food-entr-cmd 1 --food "Green Apple" --calories 80
```

#### Delete Food Entry

```bash
python -m myapp.cli food delete-food-entry-cmd <entry_id>
```

**Example:**

```bash
python -m myapp.cli food delete-food-entry-cmd 1
```

### 🎯 Goal Commands

#### Add Goal

```bash
python -m myapp.cli goal add-goal <user_id> <daily_calories> <weekly_calories>
```

**Example:**

```bash
python -m myapp.cli goal add-goal 1 2000 14000
```

#### List Goals

```bash
python -m myapp.cli goal list-goals <user_id>
```

**Example:**

```bash
python -m myapp.cli goal list-goals 1
```

#### Update Goal

```bash
python -m myapp.cli goal update-goal-cmd <goal_id> [--daily <amount>] [--weekly <amount>]
```

**Example:**

```bash
python -m myapp.cli goal update-goal-cmd 1 --daily 2200 --weekly 15400
```

#### Delete Goal

```bash
python -m myapp.cli goal delete-goal-cmd <goal_id>
```

**Example:**

```bash
python -m myapp.cli goal delete-goal-cmd 1
```

### 📅 Meal Plan Commands

#### Add Meal Plan

```bash
python -m myapp.cli meal-plan add-meal-plan <user_id> <week_number> "<meal_plan_text>"
```

**Example:**

```bash
python -m myapp.cli meal-plan add-meal-plan 1 1 "Monday: Oats, Salad, Chicken. Tuesday: Yogurt, Soup, Fish."
```

#### List Meal Plans

```bash
python -m myapp.cli meal-plan list-meal-plans <user_id>
```

**Example:**

```bash
python -m myapp.cli meal-plan list-meal-plans 1
```

#### Update Meal Plan

```bash
python -m myapp.cli meal-plan update-meal-plan-cmd <plan_id> [--week <number>] [--plan "<text>"]
```

**Example:**

```bash
python -m myapp.cli meal-plan update-meal-plan-cmd 1 --week 2 --plan "Updated meal plan"
```

#### Delete Meal Plan

```bash
python -m myapp.cli meal-plan delete-meal-plan-cmd <plan_id>
```

**Example:**

```bash
python -m myapp.cli meal-plan delete-meal-plan-cmd 1
```

### 📊 Report Commands

#### Generate User Report

```bash
python -m myapp.cli report user-report <user_id> <start_date> <end_date>
```

**Example:**

```bash
python -m myapp.cli report user-report 1 "2024-01-01" "2024-01-31"
```

**Sample Output:**

```
📋 Report for User ID 1 from 2024-01-01 to 2024-01-31:

Total entries: 25
Total calories: 52,500
```

## 🗄️ Database Schema

The application uses SQLite with SQLAlchemy ORM. The database consists of four main tables:

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);
```

### Food Entries Table

```sql
CREATE TABLE food_entries (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    food VARCHAR NOT NULL,
    calories INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Goals Table

```sql
CREATE TABLE goals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    daily INTEGER NOT NULL,
    weekly INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Meal Plans Table

```sql
CREATE TABLE meal_plans (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    week INTEGER NOT NULL,
    plan VARCHAR NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Relationships

- **One-to-Many**: User → Food Entries
- **One-to-Many**: User → Goals
- **One-to-Many**: User → Meal Plans
- **Cascade Delete**: Deleting a user removes all associated records

## 🧪 Testing

The project includes an essential test suite with 22 tests covering core functionality, CLI commands, and report generation.

### Essential Test Files

- **Core Tests** (`tests/test_essential.py`): Essential functionality tests for models, controllers, and database operations
- **CLI Tests** (`tests/test_cli_essential.py`): Essential CLI command tests
- **Report Tests** (`test_report.py`): Tests for the report generation functionality

### Running Tests

#### Install Test Dependencies

```bash
poetry install  # Includes dev dependencies
```

#### Run Essential Tests

```bash
python run_tests.py
```

This will run all essential tests and provide a summary of the results.

#### Run Individual Test Files

```bash
# Core functionality tests
pytest tests/test_essential.py -v

# CLI tests
pytest tests/test_cli_essential.py -v

# Report tests
pytest test_report.py -v
```

#### Run Tests with Coverage

```bash
pytest tests/test_essential.py tests/test_cli_essential.py test_report.py -v --cov=myapp --cov-report=term-missing
```

### Test Coverage

The essential test suite achieves good coverage across the core functionality:

- ✅ **Models**: User, FoodEntry, Goal, MealPlan
- ✅ **Controllers**: Basic CRUD operations
- ✅ **CLI Commands**: User and food management
- ✅ **Report Generation**: Nutrition reports with date ranges
- ✅ **Database**: Connection and basic operations

## 🏗️ Project Structure

```
health_tracker_cli_app/
├── myapp/                          # Main application package
│   ├── __init__.py
│   ├── cli/                        # CLI command modules
│   │   ├── __init__.py
│   │   ├── __main__.py            # Main CLI entry point
│   │   ├── user.py                # User management commands
│   │   ├── food.py                # Food tracking commands
│   │   ├── goal.py                # Goal management commands
│   │   ├── meal_plan.py           # Meal planning commands
│   │   └── report.py              # Reporting commands
│   ├── controllers/               # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_controller.py     # User CRUD operations
│   │   ├── food_entry_controller.py # Food entry operations
│   │   ├── goal_controller.py     # Goal operations
│   │   ├── meal_plan_controller.py # Meal plan operations
│   │   └── report_controller.py   # Report generation
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   ├── food_entry.py          # Food entry model
│   │   ├── goal.py                # Goal model
│   │   └── meal_plan.py           # Meal plan model
│   └── db/                        # Database configuration
│       ├── __init__.py
│       ├── database.py            # Database setup and config
│       └── db.py                  # Database session management
├── tests/                         # Comprehensive test suite
│   ├── conftest.py               # Test configuration and fixtures
│   ├── test_models/              # Model unit tests
│   ├── test_controllers/         # Controller integration tests
│   ├── test_cli/                 # CLI command tests
│   └── test_database/            # Database functionality tests
├── create_tables.py              # Database initialization script
├── run_tests.py                  # Test runner script
├── pyproject.toml               # Poetry configuration
├── pytest.ini                  # Pytest configuration
└── README.md                    # Project documentation
```

## 🛠️ Development

### Architecture

The application follows a layered architecture pattern:

1. **CLI Layer** (`myapp/cli/`): Command-line interface using Typer
2. **Controller Layer** (`myapp/controllers/`): Business logic and data processing
3. **Model Layer** (`myapp/models/`): Data models using SQLAlchemy ORM
4. **Database Layer** (`myapp/db/`): Database configuration and session management

### Design Patterns Used

- **Repository Pattern**: Controllers act as repositories for data access
- **Command Pattern**: CLI commands encapsulate user actions
- **Factory Pattern**: Database session creation
- **Dependency Injection**: Database sessions injected into controllers

### Key Technologies

- **Python 3.12+**: Modern Python features and type hints
- **Typer**: Modern CLI framework with automatic help generation
- **SQLAlchemy 2.0**: Modern ORM with async support
- **SQLite**: Lightweight, file-based database
- **Pytest**: Comprehensive testing framework
- **Poetry**: Modern dependency management

### Adding New Features

1. **Add Model**: Create new SQLAlchemy model in `myapp/models/`
2. **Add Controller**: Implement business logic in `myapp/controllers/`
3. **Add CLI Commands**: Create user interface in `myapp/cli/`
4. **Add Tests**: Write comprehensive tests in `tests/`
5. **Update Database**: Run migrations if schema changes

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions small and focused on single responsibility

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/health_tracker_cli_app.git
   cd health_tracker_cli_app
   ```
3. **Install dependencies**:
   ```bash
   poetry install
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Development Workflow

1. **Make your changes**
2. **Write tests** for new functionality
3. **Run tests** to ensure everything works:
   ```bash
   pytest tests/
   ```
4. **Run linting** (if configured):
   ```bash
   flake8 myapp/
   ```
5. **Commit your changes**:
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**

### Contribution Guidelines

- **Write Tests**: All new features must include comprehensive tests
- **Documentation**: Update README and docstrings as needed
- **Code Quality**: Follow existing code style and patterns
- **Small PRs**: Keep pull requests focused and manageable
- **Descriptive Commits**: Use clear, descriptive commit messages

### Types of Contributions

- 🐛 **Bug Fixes**: Fix existing issues
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation
- 🧪 **Tests**: Add or improve test coverage
- 🎨 **Code Quality**: Refactoring and improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Godwin Mayodi** - [godwin.mayodi@student.moringaschool.com](mailto:godwin.mayodi@student.moringaschool.com)

## 🙏 Acknowledgments

- Built as a comprehensive hands-on exercise for students
- Demonstrates OOP design patterns, SQLAlchemy ORM, and CLI tooling in Python
- Inspired by modern health and nutrition tracking applications

---

**Happy Health Tracking! 🏃‍♂️💪**
