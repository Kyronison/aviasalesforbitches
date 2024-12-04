from flask import Flask
from app.website.blueprints.auth import auth_bp
from app.website.blueprints.main import main_bp
from app.website.blueprints.cards import cards_bp

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY='pGy5lNdVGMf6pGy5lNdVGMf6'
    )
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(cards_bp, url_prefix="/cards")

    return app
