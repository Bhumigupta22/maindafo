from flask import Flask
from flask_cors import CORS
from app.database import init_db

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    from app.routes import shopping_routes, voice_routes, suggestion_routes, apriori_routes
    app.register_blueprint(shopping_routes.bp)
    app.register_blueprint(voice_routes.bp)
    app.register_blueprint(suggestion_routes.bp)
    app.register_blueprint(apriori_routes.bp)
    
    return app
