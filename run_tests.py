#!/usr/bin/env python3
"""
Test runner script for the health tracker CLI app.
"""
import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    print(f"Return code: {result.returncode}")
    return result.returncode == 0


def main():
    """Main test runner function."""
    print("Health Tracker CLI App - Test Runner")
    print("====================================")

    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Working directory: {project_dir}")

    # Test commands to run - only essential tests
    test_commands = [
        ("pytest --version", "Check pytest installation"),
        ("pytest tests/test_essential.py -v -p no:warnings", "Run essential core tests"),
        ("pytest tests/test_cli_essential.py -v -p no:warnings", "Run essential CLI tests"),
        ("pytest test_report.py -v -p no:warnings", "Run report tests"),
        ("pytest tests/test_essential.py tests/test_cli_essential.py test_report.py -v -p no:warnings --cov=myapp --cov-report=term-missing", "Run all essential tests with coverage"),
    ]

    # Run each test command
    results = []
    for command, description in test_commands:
        success = run_command(command, description)
        results.append((description, success))

    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")

    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status}: {description}")

    # Overall result
    all_passed = all(success for _, success in results)
    if all_passed:
        print(f"\n🎉 All tests completed successfully!")
        return 0
    else:
        print(f"\n❌ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
