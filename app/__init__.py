from flask import Flask
from .analyzer import bp as analyzer_bp

def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )
    app.register_blueprint(analyzer_bp)
    return app
