from flask import Blueprint

# Define the blueprint for patients_record routes
patients_bp = Blueprint('patients_record', __name__)

# Import the routes
from . import patients_routes