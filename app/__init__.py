from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    from app import database
    database.init_app(app)

    from app.auth.views import bp as auth
    app.register_blueprint(auth)

    return app
