from flask import request, jsonify, abort
from flask_jwt_extended import (jwt_required, create_access_token,
                                jwt_refresh_token_required,
                                create_refresh_token, get_jwt_identity)
from logger.manager import Multilog
from apps import jwt, app
from utils import connection
from utils.libs import build_msg, sanitizer
from flasgger import swag_from
from flask_babel import lazy_gettext as _
from utils.libs import send_task_sworn_declaration
from utils.workers import register_logger
from apps.auth import auth_server
from apps.auth.models import Login
import sys

log = Multilog(__name__).getLogger()


@swag_from('docs/login.yml')
def login():
    """
    Metodo para obtener un token y refresh_token
    :return: json - obj con las claves "token" y "refresh_token"
    """
    status = 'active'
    msg = None
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    try:
        if not request.is_json:
            msg = build_msg(error_code=400, msg='Missing JSON in request')
            custom_res['data'] = msg.data.decode()
            custom_res['code'] = 400
            raise ValueError(400)

        merge, msg = sanitizer(base={}, data=request.json, types=Login)
        if msg is not True:
            raise ValueError(400)

        if not connection.check_user_session(merge['user_id'], status, merge['session_id']):
            msg = build_msg(error_code=403, msg='Bad user_id or session_id')
            custom_res['data'] = msg.data.decode()
            custom_res['code'] = 403
            raise ValueError(403)

        msg = jsonify({
            'access_token': create_access_token(identity=merge['user_id']),
            'refresh_token': create_refresh_token(identity=merge['user_id'])
        })
        custom_res['data'] = msg.data.decode()
        custom_res['id_user'] = merge['user_id']
    except ValueError:
        log.error("Exception on auth.controller - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)
    return msg, custom_res['code']


@jwt_refresh_token_required
@swag_from('docs/refresh.yml')
def refresh():
    current_user = get_jwt_identity()
    res = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(res), 200


def sworn_declarations():
    """
    :return: json - int : msg and code from api Celery
    """
    # register_logger(kw=request, id_user=1, mode='IN')
    if not request.is_json:
        return build_msg(error_code=400, msg='Missing JSON in request',
                         data={'user_id': 1, 'type_operation': 1}), 400

    user_id = request.json.get('user_id', None)
    type_operation = request.json.get('type_operation', None)

    if not user_id:
        return build_msg(error_code=400, msg='Missing user_id parameter',
                         data={'user_id': 1, 'type_operation': 1}), 400
    if not type_operation:
        return build_msg(error_code=400, msg='Missing type_operation parameter',
                         data={'user_id': 1, 'type_operation': 1}), 400

    res, code = send_task_sworn_declaration(user_id, type_operation)

    if code == 202:
        return build_msg(error_code=202, msg=res['msg']), 202
    return build_msg(error_code=code, msg='Request error'), code


@jwt.expired_token_loader
def expired_token_callback():
    """--
    :return: custom message for JWT expired_token_loader
    """
    return build_msg(error_code=401, msg='The token has expired'), 401


@jwt.invalid_token_loader
def invalid_token_loader_callback(callback):
    """--
    :return: custom message for JWT invalid_token_loader
    """
    return build_msg(error_code=422, msg='Invalid token loader'), 422


@jwt.unauthorized_loader
def unauthorized_loader_callback(callback):
    """
    :return: custom message for JWT unauthorized_loader
    """
    return build_msg(error_code=401, msg='Unauthorized loader'), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_loader_callback():
    """
    :return: custom message for JWT needs_fresh_token_loader
    """
    return build_msg(error_code=401, msg='Needs fresh token loader'), 401


@jwt.revoked_token_loader
def revoked_token_loader_callback():
    """
    :return: custom message for JWT revoked_token_loader
    """
    return build_msg(error_code=401, msg='Revoked token loader'), 401


@jwt.user_loader_callback_loader
def user_loader_callback_loader_callback(callback):
    """
    :return: custom message for JWT user_loader_callback_loader
    """
    return build_msg(error_code=401, msg='Error loading for user '), 401


@jwt.token_in_blacklist_loader
def token_in_blacklist_loader_callback():
    """
    :return: custom message for JWT token_in_blacklist_loader
    """
    return build_msg(error_code=401, msg='Token in blacklist loader'), 401


@jwt.claims_verification_loader
def claims_verification_loader_callback(callback):
    """
    :return: custom message for JWT claims_verification_loader
    """
    return build_msg(error_code=401, msg='Claims verification loader'), 401


@jwt.claims_verification_failed_loader
def claims_verification_failed_loader_callback():
    """
    :return: custom message for JWT claims_verification_failed_loader
    """
    return build_msg(error_code=401, msg='claims verification failed loader'), 401


def callback():
    """
    método comodín
    :return:
    """
    return None


@app.errorhandler(400)
def custom400(e):
    """
    Bad Request
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=400, msg=str(e)), 400


@app.errorhandler(401)
def custom401(e):
    """
    Unauthorized
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=401, msg=str(e)), 401


@app.errorhandler(403)
def custom403(e):
    """
    Forbidden
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=403, msg=str(e)), 403


@app.errorhandler(404)
def custom404(e):
    """
    Not Found
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=404, msg=str(e)), 404


@app.errorhandler(405)
def custom405(e):
    """
    Method Not Allowed
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=405, msg=str(e)), 405


@app.errorhandler(406)
def custom406(e):
    """
    Not Acceptable
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=406, msg=str(e)), 406


@app.errorhandler(409)
def custom409(e):
    """
    Conflict
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=409, msg=str(e)), 409


@app.errorhandler(410)
def custom410(e):
    """
    Gone
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=410, msg=str(e)), 410


@app.errorhandler(500)
def custom500(e):
    """
    Internal Server Error
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=500, msg=_(str(e))), 500


@app.errorhandler(501)
def custom501(e):
    """
    Not Implemented
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=501, msg=str(e)), 501


@app.errorhandler(502)
def custom502(e):
    """
    Bad Gateway
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=502, msg=str(e)), 502


@app.errorhandler(503)
def custom503(e):
    """
    Service Unavailable
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=503, msg=str(e)), 503


@app.errorhandler(504)
def custom504(e):
    """
    Gateway Timeout
    :param e: error
    :return: json - custom message
    """
    return build_msg(error_code=504, msg=str(e)), 504


@auth_server.before_request
def limit_remote_address():
    if request.remote_addr in app.config['IP_ALLOWED']:
        pass
    else:
        return build_msg(error_code=403, msg='Unauthorized',
                         data='IP Allowed'), 403
