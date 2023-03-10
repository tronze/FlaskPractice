from flask import Flask
from flask_wtf import CSRFProtect


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CSRFProtect(app)
    app.config.from_mapping(
        SECRET_KEY=')H@McQfTjWnZr4t7w!z%C*F-JaNdRgUkXp2s5v8x/A?D(G+KbPeShVmYq3t6w9z$'
    )

    from app import database
    database.init_app(app)

    from app.auth.views import bp as auth
    from app.post.views import bp as post
    app.register_blueprint(auth)
    app.register_blueprint(post)

    app.add_url_rule("/", endpoint="index")

    return app
