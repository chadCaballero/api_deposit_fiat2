from flask import request, jsonify, abort
# from flask_jwt_extended import get_jwt_identity
from flasgger import swag_from
from flask_babel import _
import sys
# from utils.libs import dataset_to_dict, resultset_to_dict, marshal_paginated
# from apps.public.v1.serializers import (CountrySchema)
# from apps.public.models import (BankData, CountryCurrencyBankPayment,
#                                 Country, Currency, PaymentMethod)
# from apps.public.v1.serializers import CountrySchema
# from apps import app, db
# from sqlalchemy.orm import load_only
from utils.connection import get_list_queryset_sp
from utils.libs import get_kwargs, get_token
from apps.auth.v1.controllers import register_logger
from logger.manager import Multilog

log = Multilog(__name__).getLogger()


@swag_from('docs/countries_per_money.yml')
def countries_per_money(id_money):
    """
    :param id_money: ID moneda para filtrar la lista de paises asociados --ok
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, )
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_country', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


@swag_from('docs/countries.yml')  # falta asignar un archivo de documentacion
def countries():
    """
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_country_all', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


@swag_from('docs/payments.yml')  # falta asignar un archivo de documentacion
def payments():
    """
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_payment_method_all', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/payments_per_moneycountry.yml')
def payments_per_moneycountry(id_money, id_country):
    """
    :param id_money:
    :param id_country:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_payment_method', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


@swag_from('docs/collectors.yml')  # falta asignar un archivo de documentacion
def collectors():
    """
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_collector_all', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/collectors_per_moneyCountryPayment.yml')
def collectors_per_moneyCountryPayment(id_money, id_country, id_payment):
    """
    :param id_money:
    :param id_country:
    :param id_payment:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_payment)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_collector', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/commissions_per_moneycountrypaymentcollector.yml')
def commissions_per_moneycountrypaymentcollector(id_money, id_country, id_payment, id_collect):
    """
    :param id_money:
    :param id_country:
    :param id_payment:
    :param id_collect:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_collect, id_payment)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_commission', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/payment_instructions_per_moneycountry.yml')
def payment_instructions_per_moneycountry(id_money, id_country, id_lang):
    """
    :param id_money:
    :param id_country:
    :param id_lang:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_lang)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_info_pago_03', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/payment_instructions_per_moneycountrypaymentcollector.yml')
def payment_instructions_per_moneycountrypaymentcollector(id_money, id_country, id_payment, id_collect, id_lang):
    """
    :param id_money:
    :param id_country:
    :param id_payment:
    :param id_collect:
    :param id_lang:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_collect, id_payment, id_lang)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_info_pago_05', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/payment_instructions_per_moneycountrypaymentcollector.yml')
def payment_instructions_per_moneycountrypayment(id_money, id_country, id_payment, id_lang):
    """
    :param id_money:
    :param id_country:
    :param id_payment:
    :param id_lang:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_payment, id_lang)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_info_pago_all', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)


# @jwt_required
@swag_from('docs/payment_instructions_per_moneycountrypaymentcollector.yml')
def payment_instructions_per_moneycountrycollector(id_money, id_country, id_collect, id_lang):
    """
    :param id_money:
    :param id_country:
    :param id_collect:
    :param id_lang:
    :return:
    """
    custom_res = dict()
    kwargs = get_kwargs(request, id_money, id_country, id_collect, id_lang)
    if kwargs:
        res = get_list_queryset_sp(sp_name='sp_list_info_pago_04', pagination=True, **kwargs)
        custom_res['data'] = str(res)
        custom_res['code'] = 200 if res else 500
        register_logger(rekuest=request, response=custom_res)
        return jsonify(res) if res else abort(500)
    abort(500)
