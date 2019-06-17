from flask import Blueprint

auth_server = Blueprint('auth', __name__)

from apps.auth.v1 import routes
