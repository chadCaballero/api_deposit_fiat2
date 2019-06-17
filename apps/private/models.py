# from _datetime import datetime
from apps import db

"""
TIPOS:
    - int()
    - float() => Decimal
    - str() => ""
    - None => null
    - list() => []
    - dict() => {}
    - tupla con todos los tipos permitidos ejm: (float(), int(), str())
"""


class Deposit(object):
    user_id = int()


class DepositRequest(Deposit):
    platform = str()
    money = int()
    country = int()
    payment_method = int()
    collector = int()
    mount = (float(), int())


class DepositCheck(Deposit):
    deposit = int()
    deposit_date = str()
    deposit_name = str()
    tel = int()
    cta = int()
    operation_num = int()
    voucher = str()


class DepositCancel(Deposit):
    deposit = (int(), float())


class DepositReject(Deposit):
    user = int()
    username = str()
    password = str()
    deposit = (int(), float())


class DepositAccept(Deposit):
    deposit = int()
    username = str()
    password = str()
    voucher = str()


class CountryMoney(object):
    status = bool()


class InfoDeposit(db.Model):
    __tablename__ = "dep_info_pago"

    idPago = db.Column(db.Integer, primary_key=True)
    idCurrency = db.Column(db.Integer)
    idCountry = db.Column(db.Integer)
    idCollector = db.Column(db.Integer)
    idPayment = db.Column(db.Integer)
    max_amount = db.Column(db.Float)
    min_amount = db.Column(db.Float)


class PayLanguage(db.Model):
    __tablename__ = "dep_pago_language"

    iD = db.Column(db.Integer, primary_key=True)
    idLanguage = db.Column(db.Integer)
    idPago = db.Column(db.Integer)
    description = db.Column(db.Integer)


