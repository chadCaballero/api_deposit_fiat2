from apps.private.models import (DepositRequest, DepositAccept,
                                 DepositCancel, DepositCheck,
                                 DepositReject, CountryMoney)
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from utils.libs import get_kwargs, build_msg_dict
from utils import connection
from utils.libs import sanitizer
from apps.auth.v1.controllers import register_logger
from logger.manager import Multilog
import sys

log = Multilog(__name__).getLogger()


# (1)
@jwt_required
@swag_from('docs/requests_deposit.yml')
def deposit_per_platform(platform):
    """
    :param platform:
    :return:
    """
    custom_res = dict()
    custom_res['id_user'] = get_jwt_identity()
    kwargs = get_kwargs(request, platform, )
    if kwargs:
        res = connection.get_list_queryset_sp(sp_name='sp_list_payment_method', **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# (2)
@jwt_required
@swag_from(
    'docs/deposit_per_platformmoneycountrypaymentcollectorstatus.yml')
def deposit_per_platformmoneycountrypaymentcollectorstatus(platform, id_money, id_country, id_payment, id_collect,
                                                           status):
    """
    :param platform:
    :param id_money:
    :param id_country:
    :param id_payment:
    :param id_collect:
    :param status:
    :return:
    """
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200

    try:
        kwargs = get_kwargs(request, get_jwt_identity(), id_money, status, id_country, id_payment, id_collect)
        if kwargs:
            res = connection.get_list_queryset_sp(sp_name='sp_listar_depositos', **kwargs)
            if res:
                custom_res['data'] = res
                custom_res['code'] = 200
            else:
                custom_res['data'] = build_msg_dict(error_code=404, msg='error sp')
                custom_res['code'] = 404
                raise ValueError(404)
        else:
            custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
            custom_res['code'] = 500
            raise ValueError(500)

    except ValueError:
        log.error("Exception on deposits_cancel_delay - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)

    return jsonify(custom_res['data']), custom_res['code']


# (3)
@jwt_required
@swag_from('docs/deposits.yml')
def deposits_post():
    params = dict()
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    params['user'] = get_jwt_identity()

    try:
        merge, msg = sanitizer(base=params, data=request.json, types=DepositRequest)
        if msg is not True:
            custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
            custom_res['code'] = 400
            raise ValueError(400)

        kwargs = get_kwargs(request, merge['mount'], merge['money'], merge['payment_method'],
                            merge['collector'], merge['user'])
        if kwargs:
            res = connection.get_queryset_upsert_sp(sp_name='sp_solicitud_deposito', **kwargs)
            if res:
                custom_res['data'] = res
                custom_res['code'] = 201
            else:
                custom_res['data'] = build_msg_dict(error_code=500, msg='error sp')
                custom_res['code'] = 500
                raise ValueError(500)
        else:
            custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
            custom_res['code'] = 500
            raise ValueError(500)

    except ValueError:
        log.error("Exception on deposits_cancel_delay - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)

    return jsonify(custom_res['data']), custom_res['code']


# (3.1)
@swag_from('docs/deposits.yml')
def deposits_put():
    params = dict()
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    res = None
    action = request.json.get('action', None)
    try:
        if action == 'check':
            """
            require JWT
            """
            return deposits_verify_delay()

        elif action == 'cancel':
            """
            require JWT
            """
            return deposits_cancel_delay()

        elif action == 'reject':
            """
            """
            merge, msg = sanitizer(base={}, data=request.json, types=DepositReject)
            if msg is not True:
                custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
                custom_res['code'] = 400
                raise ValueError(400)

            if not connection.check_sub_admin(merge['username'], 'active', merge['password'], '1'):
                custom_res['data'] = build_msg_dict(error_code=403, msg='Bad user, password, status or permission')
                custom_res['code'] = 403
                raise ValueError(403)

            kwargs = get_kwargs(request, merge['user'], merge['deposit'])
            if kwargs:
                res = connection.get_queryset_upsert_sp(sp_name='sp_reject_deposit', **kwargs)
                if res:
                    custom_res['data'] = res
                    custom_res['code'] = 200
                else:
                    custom_res['data'] = build_msg_dict(error_code=500, msg='error sp')
                    custom_res['code'] = 500
                    raise ValueError(500)
            else:
                custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
                custom_res['code'] = 500
                raise ValueError(500)

        elif action == 'accept':
            """
            probado, por replicar en los demás
            """

            merge, msg = sanitizer(base={}, data=request.json, types=DepositAccept)
            if msg is not True:
                custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
                custom_res['code'] = 400
                raise ValueError(400)

            if not connection.check_sub_admin(merge['username'], 'active', merge['password'], '1'):
                custom_res['data'] = build_msg_dict(error_code=403, msg='Bad user, password, status or permission')
                custom_res['code'] = 403
                raise ValueError(403)

            # PidDeposit
            # int, IN
            # Puserid
            # int, IN
            # Pcomprobante
            # text, IN
            # Pestado
            # int)
            kwargs = get_kwargs(request, merge['deposit'], merge['username'], merge['password'],
                                merge['voucher'])
            if kwargs:
                res = connection.get_queryset_upsert_sp(sp_name='sp_approved_deposit', **kwargs)
                if res:
                    custom_res['data'] = res
                    custom_res['code'] = 201
                else:
                    custom_res['data'] = build_msg_dict(error_code=500, msg='error sp')
                    custom_res['code'] = 500
                    raise ValueError(500)
            else:
                custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
                custom_res['code'] = 500
                raise ValueError(500)

        elif action is None:

            abort(400, 'Argument "Action" not found')
        else:

            abort(400, 'Action not permissive')

    except ValueError:
        log.error("Exception on auth.controller - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)

    return jsonify(custom_res['data']), custom_res['code']


# (3.2)
@jwt_required
@swag_from('docs/deposits_cancel.yml')
def deposits_cancel_delay():
    params = dict()
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    params['user'] = get_jwt_identity()

    try:
        merge, msg = sanitizer(base=params, data=request.json, types=DepositCancel)
        if msg is not True:
            custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
            custom_res['code'] = 400
            raise ValueError(400)

        kwargs = get_kwargs(request, merge['user'], merge['deposit'])
        if kwargs:
            res = connection.get_queryset_upsert_sp(sp_name='sp_cancel_deposit', **kwargs)
            if res:
                custom_res['data'] = res
                custom_res['code'] = 201
            else:
                custom_res['data'] = build_msg_dict(error_code=500, msg='error sp')
                custom_res['code'] = 500
                raise ValueError(500)
        else:
            custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
            custom_res['code'] = 500
            raise ValueError(500)

    except ValueError:
        log.error("Exception on deposits_cancel_delay - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)

    return jsonify(custom_res['data']), custom_res['code']


# (3.3)
@jwt_required
@swag_from('docs/deposits_verify.yml')
def deposits_verify_delay():
    params = dict()
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    params['user'] = get_jwt_identity()

    try:
        merge, msg = sanitizer(base=params, data=request.json, types=DepositCheck)
        if msg is not True:
            custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
            custom_res['code'] = 400
            raise ValueError(400)

        kwargs = get_kwargs(request, merge['user'], merge['deposit'], merge['deposit_date'],
                            merge['deposit_name'], merge['tel'], merge['cta'], merge['operation_num'],
                            merge['voucher'])
        if kwargs:
            res = connection.get_queryset_upsert_sp(sp_name='sp_verify_deposit', **kwargs)
            if res:
                custom_res['data'] = res
                custom_res['code'] = 201
            else:
                custom_res['data'] = build_msg_dict(error_code=500, msg='error sp')
                custom_res['code'] = 500
                raise ValueError(500)
        else:
            custom_res['data'] = build_msg_dict(error_code=500, msg='error kwargs')
            custom_res['code'] = 500
            raise ValueError(500)

    except ValueError:
        log.error("Exception on deposits_verify_delay - code:{}".format(sys.exc_info()[1].args[0]))
    finally:
        register_logger(rekuest=request, response=custom_res)

    return jsonify(custom_res['data']), custom_res['code']


# (4)
@jwt_required
@swag_from('docs/asoc_country_with_money.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def asoc_country_with_money(id_country, id_money):
    user_id = get_jwt_identity()
    res = None
    try:
        custom_res = dict()
        custom_res['id_user'] = get_jwt_identity()
        params = dict()
        kwargs = get_kwargs(request, id_country, id_money)
        if request.method == "POST":
            if kwargs:
                res = connection.get_list_queryset_sp(sp_name='sp_tmp', **kwargs)
            else:
                custom_res['data'] = str(res)
                custom_res['code'] = 200 if res else 500
                raise ValueError(500)
        else:
            merge, msg = sanitizer(base=params, data=request.json, types=CountryMoney)
            if msg is not True:
                custom_res['data'] = str(res)
                custom_res['code'] = 400
                raise ValueError(400)
    except ValueError:
        log.error("")
    finally:
        register_logger(rekuest=request, response=custom_res)
    return jsonify(res) if res else abort(500)


# (6)
@jwt_required
@swag_from('docs/asoc_collector_with_country.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def asoc_collector_with_country(id_collect, id_country):
    pass


# (7)
@jwt_required
@swag_from('docs/collectors.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def collectors(id_collect):
    pass


# (8)
@jwt_required
@swag_from('docs/asoc_payment_with_collector.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def asoc_payment_with_collector(id_payment, id_collect):
    pass


# (9)
@jwt_required
@swag_from('docs/payments.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def payments(id_payment):
    pass


# (10 && 11)
@swag_from('docs/companies_crud.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def companies(id_company=None):

    params = dict()
    custom_res = dict()
    custom_res['data'] = ''
    custom_res['code'] = 200
    params['user'] = get_jwt_identity()

    if request.method == 'GET':
        if id_company:
            pass
        else:
            merge, msg = sanitizer(base={}, data=request.json, types=DepositReject)
            if msg is not True:
                custom_res['data'] = build_msg_dict(error_code=400, msg=msg)
                custom_res['code'] = 400
                raise ValueError(400)

            if not connection.check_sub_admin(merge['username'], 'active', merge['password'], '1'):
                custom_res['data'] = build_msg_dict(error_code=403, msg='Bad user, password, status or permission')
                custom_res['code'] = 403
                raise ValueError(403)

    elif request.method == 'POST':
        pass
    else:
        pass


# (12 && 13)
@jwt_required
@swag_from('docs/bank_data.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def bank_data(bank_data=None):
    pass


# (14)
@jwt_required
@swag_from('docs/languages.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def languages():
    pass


# (15 && 16)
@jwt_required
@swag_from('docs/instructions.yml')  # FALTA ARCHIVO DE DOCUMENTACION
def instructions(id_instruction=None):
    pass
