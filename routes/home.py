from flask import Blueprint, request, jsonify, render_template


home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def main_page():
    return render_template("home.html")


# Function to configure home routes in the Flask app
def configure_home_routes(app):
    """
    Configure and register home-related routes with a Flask app.

    Args:
    - app: Flask app instance.

    Returns:
    - auth_routes: Blueprint for home-related routes.
    """
    app.register_blueprint(home_routes)
    return home_routes
