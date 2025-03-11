from flask import Flask
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS
    CORS(app)

    # Import and register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app