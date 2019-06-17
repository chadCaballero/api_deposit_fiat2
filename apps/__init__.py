import os
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
# from flask_admin import Admin
from flask_babel import Babel
from flasgger import Swagger

app = Flask(__name__)
CORS(app)

# app.config.from_pyfile('../conf/config.py')
app_settings = os.getenv(
    'APP_SETTINGS',
    'apps.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# db = SQLAlchemy(app, session_options={'autocommit': True})
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)
swagger = Swagger(app)
# admin = Admin(app, name='Api deposit fiat', template_mode='bootstrap3')
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"].keys())
    # translations = [str(translation) for translation in babel.list_translations()]
    # return request.accept_languages.best_match(translations)


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone


from apps.public import endpoints_publics
from apps.private import endpoints_privates
from apps.auth import auth_server

app.register_blueprint(endpoints_publics, url_prefix='/v1')
app.register_blueprint(endpoints_privates, url_prefix='/v1')
app.register_blueprint(auth_server, url_prefix='/v1')
