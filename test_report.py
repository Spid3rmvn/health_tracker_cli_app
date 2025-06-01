from datetime import date, datetime
from myapp.db.db import get_db
from myapp.controllers.report_controller import generate_user_report
from myapp.controllers.user_controller import create_user
from myapp.controllers.food_entry_controller import create_food_entry
from myapp.controllers.goal_controller import create_goal

def test_report():
    """Test the enhanced report functionality."""
    with get_db() as db:
        # Create a test user with a unique name using timestamp
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        user = create_user(db, f"test_user_report_{timestamp}")

        # Create a goal for the user
        goal = create_goal(db, user.id, 2000, 14000)

        # Create some food entries for the user
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 7)

        # Day 1
        create_food_entry(db, user.id, "Breakfast", 500, start_date)
        create_food_entry(db, user.id, "Lunch", 700, start_date)
        create_food_entry(db, user.id, "Dinner", 800, start_date)

        # Day 2
        create_food_entry(db, user.id, "Breakfast", 400, date(2024, 1, 2))
        create_food_entry(db, user.id, "Lunch", 600, date(2024, 1, 2))

        # Day 4
        create_food_entry(db, user.id, "Breakfast", 450, date(2024, 1, 4))
        create_food_entry(db, user.id, "Lunch", 650, date(2024, 1, 4))
        create_food_entry(db, user.id, "Dinner", 750, date(2024, 1, 4))

        # Day 7
        create_food_entry(db, user.id, "Breakfast", 500, end_date)
        create_food_entry(db, user.id, "Dinner", 900, end_date)

        # Generate the report
        report = generate_user_report(db, user.id, start_date, end_date)

        # Print the report
        print("\n📋 NUTRITION REPORT for User ID", user.id)
        print(f"📅 Period: {start_date} to {end_date} ({report['days_in_period']} days)")
        print("=" * 50)

        print("\n📊 SUMMARY STATISTICS")
        print(f"Total entries: {report['total_entries']}")
        print(f"Total calories: {report['total_calories']:,}")
        print(f"Days tracked: {report['days_tracked']} of {report['days_in_period']} ({report['tracking_consistency']}% consistency)")
        print(f"Average daily calories: {report['avg_daily_calories']:,}")

        if report.get('has_goal', False):
            print("\n🎯 GOAL COMPARISON")
            print(f"Daily calorie goal: {report['daily_goal']:,}")
            if 'daily_goal_percent' in report:
                goal_status = "✅ Under goal" if report['daily_goal_percent'] <= 100 else "❌ Over goal"
                print(f"Daily average: {report['avg_daily_calories']:,} calories ({report['daily_goal_percent']}% of goal) {goal_status}")

            print(f"Weekly calorie goal: {report['weekly_goal']:,}")
            if 'weekly_goal_percent' in report:
                weekly_goal_status = "✅ Under goal" if report['weekly_goal_percent'] <= 100 else "❌ Over goal"
                print(f"Weekly average: {report['weekly_avg_calories']:,} calories ({report['weekly_goal_percent']}% of goal) {weekly_goal_status}")

        if report.get('daily_breakdown') and len(report['daily_breakdown']) > 0:
            print("\n📆 DAILY BREAKDOWN")
            for date_str, calories in report['daily_breakdown'].items():
                print(f"{date_str}: {calories:,} calories")

if __name__ == "__main__":
    test_report()
