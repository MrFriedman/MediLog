from flask import Blueprint

# Define the blueprint for provider admin routes
provider_bp = Blueprint('provider', __name__)

# Import the routes
from . import provider_routes