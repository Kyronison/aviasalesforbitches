from flask import Flask
import os
def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config.update(
        SECRET_KEY='pGy5lNdVGMf6pGy5lNdVGMf6'
    )
    return app
