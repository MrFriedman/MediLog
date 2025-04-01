from flask import Blueprint

# Define the blueprint for admin routes
doctor_bp = Blueprint('doctor', __name__)

# Import the routes
from . import admin_routes