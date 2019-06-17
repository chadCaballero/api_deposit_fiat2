__author__ = "Mark"
__copyright__ = "Copyright 2018,"
__credits__ = ["Marco Antonio"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mark"
__email__ = "mmena@bitinka.com"
__status__ = "Development"

from utils.paginator import paginated_dict
from apps.config import (ERROR_MSG_TEMPLATE, TOKEN_FILE_NAME, TOKEN_BASE,
                         URL_API_CELERY_LOGIN, LOGGER_CONFIG, USER_API, PASS_API,
                         URL_API_SWORN_DECLARATION)
from flask import jsonify, abort
from apps import app
import os, platform, base64, json, time, requests, pickle
from datetime import datetime
from decimal import Decimal
from flask_babel import _, lazy_gettext as __

fn_custom_str = lambda s: "'{}'".format(s) if isinstance(s, str) else str(s)
"""
    :param s: un parametro de tipado dinámico
           - metodo customizado para que los parametros de los store procedures que son VARCHAR,
             se concatenen con comillas simples
"""

fn_format_args = lambda s, **kw: 'call ' + s + '({})'.format(
    ','.join(map(fn_custom_str, kw['args_sp']))) if 'args_sp' in kw else None
"""
    :param s: nombre del store procedure
    :param **kw: tuple or list - diccionario con la llave args_sp que contiene todos los parametros del SP
    :return: str - cadena completa
"""

fn_decimal_to_float = lambda s: float(s) if isinstance(s, Decimal) else __(s)  # with translate
# fn_decimal_to_float = lambda s: float(s) if isinstance(s, Decimal) else s
"""
    :param s: un parametro de tipado dinámico
           - metodo customizado para convertir los objetos Decimal a float
"""


def build_msg(**kwargs):
    """
    Los endpoints deben manejar una lista de errores por código indicando el módulo del fallo y un identificador. Para
    las respuestas deben manejar el siguiente formato:

    success     (Boolean):  Indica si la transacción resultó exitosa.
    msg         (String):   Mensaje dirigido al usuario indicando el resultado de la transacción.
    error_code  (String):   Código de error de respuesta.
    data        (Array):    Arreglo de datos necesarios por el endpoint. En caso de error o de no ser necesario el retorno
                            de datos, debe mostrar False.
    :return:    json message
    """
    return jsonify({**ERROR_MSG_TEMPLATE, **kwargs})


def build_msg_dict(**kwargs):
    return {**ERROR_MSG_TEMPLATE, **kwargs}


def get_kwargs(rekuest=None, *args):
    """
    :param rekuest: obj global request from flask
    :param args: tuple with all params
    :return: dict **kwargs
    """
    try:
        return {'start': int(rekuest.args.get('start', app.config['PAGINATION_START'])),
                'limit': int(rekuest.args.get('limit', app.config['PAGINATION_LIMIT'])),
                'url_base': rekuest.base_url, 'args_sp': args} if rekuest else {'args_sp': args}
    except Exception:
        return None


def dataset_to_dict(dataset=None, pagination=False, **kwargs):
    """
    :param dataset: lista de tuplas resultado de SqlAlchemy
    :param pagination: condicion para devolver paginado
    :return: objeto dict
    """
    if dataset.returns_rows:
        keys = dataset.keys()
        table = dataset.fetchall()

        sanitized = [map(fn_decimal_to_float, t) for t in table]

        res = [dict(zip(keys, row)) for row in sanitized]
        return paginated_dict(res, **kwargs) if pagination else res
    else:
        return paginated_dict([], **kwargs) if pagination else []


def resultset_to_dict(resultset=None, pagination=False, **kwargs):
    """
    :param resultset: result query SqlAlchemy on Model
    :param pagination: condicion para devolver el resultado paginado
    :param kwargs: parametros opcionales
    :return: objeto dict
    """
    if resultset:
        keys = resultset[:1][0].__table__.columns.keys()
        res = [dict(zip(keys, row.get_args())) for row in resultset]
    return paginated_dict(res, **kwargs) if pagination else res


def marshal_paginated(marshal=None, pagination=False, **kwargs):
    """
    :param marshal: objeto Marshmellow
    :param pagination: condicion para devolver el resultado paginado
    :param kwargs: parametros opcionales para la paginacion
    :return: objeto dict
    """
    return paginated_dict(marshal, **kwargs) if marshal else None


def send_task_sworn_declaration(id_user=None, type_operation=None):
    """
    Se debe crear una tarea que permita hacer uso del store que hace las validaciones si un usuario amerita declaración,
    de acuerdo al tipo de operación que está realizando. Debe recibir: id de usuario y tipo de operación ( 1: Depósito
    Fiat, 2: Retiro Fiat, 3 Retiro Cripto )
    :return:
    """
    body = json.dumps({'user_id': id_user, 'type_operation': type_operation})
    res = request_to_url_post(url=URL_API_SWORN_DECLARATION, data=body)
    return res.json(), res.status_code


def get_token():
    """
    Método para obtener el token de acceso al API ....declaracion jurada...¿?
    :return:
    """
    path_file = os.path.join(get_path_home(), LOGGER_CONFIG['log_folder'], TOKEN_FILE_NAME)
    token = read_bin_file(path_file)
    exp = get_exp_token(token)
    if exp < 5:  # 5 segundos
        cont = 0
        body = json.dumps({'username': USER_API, 'password': PASS_API})
        while cont < 3:
            response = request_to_url_post(url=URL_API_CELERY_LOGIN, data=body)
            if response.status_code == 200:
                write_bin_file(file=path_file, data=response.json()['access_token'])
                return response.json()['access_token']
            else:
                cont += 1
                time.sleep(cont / 2)
        return None
    return token


def request_to_url_get(url, attempts=2, headers={'Content-Type': 'application/json'}):
    """
    :param url: str - unico parametro obligatorio, endpoint público
    :param attempts: int - numero de veces a intentar
    :param headers: dict - cabeceras HTTP
    :return: depende del Content-type: HTML -> str, JSON -> Json
    """
    cont = 0
    while cont < attempts:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                content_type = response.headers['content-type']
                if 'application/json' in content_type:
                    # por definir
                    return response.json()
                elif 'text/html' in content_type:
                    return str(json.loads(response.text)['data'])
            else:
                cont += 1
                time.sleep(cont / 2)
        except Exception:
            return None
    return None


def request_to_url_post(url, data):
    return requests.post(url, data=data, headers={'Content-Type': 'application/json'})


def get_exp_token(token):
    """
    :param token: str - JWT en formato x.x.x
    :return: int - tiempo restante para que expire el token en formato UNIX
    """
    payload = token.split('.')[1].encode()
    dic = json.loads(decode_base64(payload))
    exp = dic['exp']
    unixstamp = time.mktime(datetime.now().timetuple())
    return exp - unixstamp


def read_flat_file(file=None):
    """
    :param file: nombre del archivo plano
    :return: iterador con todos las lineas del archivo
    """
    with open(file, 'r') as f:
        data = f.readlines()
    return data


def read_bin_file(file=None):
    """
    :param file: ruta completa del archivo binario
    :return: iterador con todos las lineas del archivo
    """
    with open(file, 'rb') as f:
        lista = pickle.load(f)
    return lista


def write_bin_file(file=None, data=None):
    """
    :param file: ruta completa del archivo binario
    :return: iterador con todos las lineas del archivo
    """
    with open(file, 'wb') as f:
        res = pickle.dump(data, f)
    return res


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    #
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return base64.decodebytes(data)


def check_resource(folder, file=None):
    """
    :param folder: nombre del folder sobre el HOME del usuario de turno sea Windows o Unix
    :param file: nombre del archivo dentro de la carpeta del primer parámetro
    :return: bool - si el recurso esta o no luego del método
    """
    folder_path = os.path.join(get_path_home(), folder)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except OSError as e:
        print('CHECK FOLDER - ERROR: ', e)
    try:
        path_file = os.path.join(folder_path, TOKEN_FILE_NAME)
        if not os.path.isfile(path_file):
            write_bin_file(file=path_file, data=TOKEN_BASE)
    except OSError as e:
        print('CHECK FILE - ERROR: ', e)


def get_path_home():
    if platform.platform().startswith('Windows'):
        folder_path = os.path.join(os.getenv('HOMEDRIVE'),
                                   os.getenv("HOMEPATH"))
    else:
        folder_path = os.path.join(os.getenv('HOME'))
    return folder_path


def sanitizer(base=None, data=None, types=object):
    attrs = dict((k, v) for k, v in types.__dict__.items() if not k.startswith('__'))
    merge = {**base, **data}
    for k, v in attrs.items():
        if isinstance(v, type(tuple())):
            if [None for _ in v if isinstance(merge[k], type(_))]:
                continue
        if k in merge:
            if isinstance(merge[k], type(v)):
                continue
            else:
                return k, "Parameter '{}' Invalid data type".format(k)
        else:
            return k, "Parameter '{}' not found".format(k)
    return merge, True
