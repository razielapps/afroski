import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "app", "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
