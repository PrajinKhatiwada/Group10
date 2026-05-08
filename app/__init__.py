from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
import os


def create_app():
    app = Flask(__name__)

    app.secret_key = os.getenv("SECRET_KEY", "PropertySalesSecretKey2024!")

    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "localhost")
    app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT", 3306))
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "root")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "9814073971")
    app.config["MYSQL_DATABASE"] = os.getenv("MYSQL_DATABASE", "property_sales")

    CSRFProtect(app)
    Bootstrap5(app)

    from . import db
    with app.app_context():
        db.init_db()

    from .views import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def not_found(e):
        return render_template(
            "error.html",
            code=404,
            message="Page not found."
        ), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template(
            "error.html",
            code=500,
            message="Internal server error. Please try again later."
        ), 500

    return app