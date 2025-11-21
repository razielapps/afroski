from flask import Flask
from config import Config
from extensions import db, login_manager
from auth import auth_bp
from listings import listings_bp
from messages import messages_bp

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(listings_bp, url_prefix="/listings")
    app.register_blueprint(messages_bp, url_prefix="/messages")
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
