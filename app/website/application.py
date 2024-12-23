from flask import Flask, render_template
from app.website.blueprints.auth import auth_bp
from app.website.blueprints.main import main_bp
from app.website.blueprints.cards import cards_bp
from app.config.secrets import Secrets


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=Secrets.get_secret('SECRET_KEY')
    )
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(cards_bp, url_prefix="/cards")

    # Глобальный обработчик ошибки 404 (страница не найдена)
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    # Глобальный обработчик ошибки 500 (внутренняя ошибка сервера)
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app
