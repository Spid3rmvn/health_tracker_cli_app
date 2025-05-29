from setuptools import setup, find_packages

setup(
    name="health_tracker_cli_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer",
        "sqlalchemy",
        # other dependencies
    ],
    entry_points={
        "console_scripts": [
            "myapp = myapp.cli.__main__:main",
        ],
    },
)
