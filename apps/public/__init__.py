from flask import Blueprint

endpoints_publics = Blueprint('public', __name__)

from apps.public.v1 import routes

