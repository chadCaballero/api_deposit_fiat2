from flask import Blueprint# from flask_admin.contrib.sqla import ModelView
# from apps import admin, db
# from apps.auth.models import Logger, UserDetails
#
# admin.add_view(ModelView(Logger, db.session))
# admin.add_view(ModelView(UserDetails, db.session))


endpoints_privates = Blueprint('private', __name__)

from apps.private.v1 import routes

