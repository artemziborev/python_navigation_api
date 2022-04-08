from flask import Flask

from src import app
from .example_routes import count_calls, list_routes


def add_routes(target_app: Flask = app) -> None:
    """Add routes to main app

    Args:
        target_app: Flask instance. Defaults app.
    """
    target_app.add_url_rule(rule='/', view_func=list_routes)
    target_app.add_url_rule(rule='/count', view_func=count_calls)
