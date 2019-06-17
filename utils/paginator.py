__author__ = "Mark"
__copyright__ = "Copyright 2018,"
__credits__ = ["Marco Antonio"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mark"
__email__ = "mmena@bitinka.com"
__status__ = "Development"

from flask import abort, jsonify


def get_paginated_list(request, resultset, serializer):
    """
    :param request: metadata de la solicitud externa
    :param resultset: dataset instance SqlAlchemy
    :param serializer: clase serializadora
    :return: lista json paginada
    """
    url = request.base_url
    start = int(request.args.get('start', 1))
    limit = int(request.args.get('limit', 10))

    # revisamos si existe datos
    count = len(resultset)
    if count < start:
        abort(404)

    # definimos las llaves
    obj = dict()
    obj['count'] = count
    obj['limit'] = limit
    obj['start'] = start

    # armamos las urls anterior y siguiente
    if start == 1:
        obj['previous'] = None
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start={}&limit={}'.format(start_copy, limit_copy)
    if start + limit > count:
        obj['next'] = None
    else:
        start_copy = start + limit
        obj['next'] = url + '?start={}&limit={}'.format(start_copy, limit)

    # hacemos slicing al resulset de Sqlalchemy acorde a lo requerido
    # obj['results'] = results[(start - 1):(start - 1 + limit)]
    schema = serializer(many=True)
    result = schema.dump(resultset[(start - 1):(start - 1 + limit)])
    obj['result'] = result.data
    return jsonify(obj)


# unico usado hasta el momento
def paginated_dict(data, **kwargs):
    """
    :param data: metadata de la solicitud externa
    :param klass: clase entidad de la base de datos para SqlAlchemy
    :param serializer: clase serializadora
    :return: lista json paginada
    """
    url = kwargs['url_base']

    if not isinstance(kwargs['start'], int):
        abort(404)
    if not isinstance(kwargs['limit'], int):
        abort(404)

    start = abs(kwargs['start'])
    limit = abs(kwargs['limit'])

    # revisamos si hay datos
    count = len(data)
    if count < start:
        pass
        # por implementar un mensaje personalizado cuando no hay datos
        # abort(404)

    # definimos las llaves
    obj = dict()
    obj['count'] = count
    obj['limit'] = limit
    obj['start'] = start

    # armamos las urls anterior y siguiente
    if start == 1:
        obj['previous'] = None
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start={}&limit={}'.format(start_copy, limit)
    if start + limit > count:
        obj['next'] = None
    else:
        start_copy = start + limit
        obj['next'] = url + '?start={}&limit={}'.format(start_copy, limit)

    obj['result'] = data[(start - 1):(start - 1 + limit)]
    return obj
