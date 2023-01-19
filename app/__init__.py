from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    return app
