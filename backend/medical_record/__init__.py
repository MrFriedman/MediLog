from flask import Blueprint

# Define the blueprint for medical_record routes
medical_record_bp = Blueprint('medical_record', __name__)

# Import the routes
from . import medical_record_routes