from flask import Blueprint

messages_bp = Blueprint("messages", __name__, template_folder="../templates")

from . import views
