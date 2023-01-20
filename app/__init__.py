from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=')H@McQfTjWnZr4t7w!z%C*F-JaNdRgUkXp2s5v8x/A?D(G+KbPeShVmYq3t6w9z$'
    )

    from app import database
    database.init_app(app)

    from app.auth.views import bp as auth
    app.register_blueprint(auth)

    app.add_url_rule("/", endpoint="index")

    return app
