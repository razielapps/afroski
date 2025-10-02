from flask import Blueprint

listings_bp = Blueprint("listings", __name__, template_folder="../templates")

from . import views
