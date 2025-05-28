from flask import Blueprint

# Define the blueprint for health_metrics_record routes
health_metrics_bp = Blueprint('health_metrics_record', __name__)

# Import the routes
from . import health_metrics_routes