from apps import db


class Country(db.Model):
    __tablename__ = "country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    status = db.Column(db.CHAR(1))

    country_currency_bank_payment = db.relationship('CountryCurrencyBankPayment',
                                                    backref='country', lazy='dynamic')

    def __repr__(self):
        return self.name

    def get_args(self):
        return self.id, self.name, self.status


class Currency(db.Model):
    __tablename__ = "currency"

    id = db.Column(db.Integer, primary_key=True)
    coin = db.Column(db.String(20))
    status = db.Column(db.Integer)
    img = db.Column(db.String(100))
    orderTrade = db.Column(db.Integer)
    link = db.Column(db.Text)
    typeCoin = db.Column(db.SmallInteger)

    country_currency_bank_payment = db.relationship('CountryCurrencyBankPayment',
                                                    backref='currency', lazy='dynamic')

    def __repr__(self):
        return self.coin

    def get_args(self):
        return (self.id, self.coin,
                self.status, self.img, self.orderTrade,
                self.link, self.typeCoin)


class BankData(db.Model):
    __tablename__ = "bank_data"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    country_currency_bank_payment = db.relationship('CountryCurrencyBankPayment',
                                                    backref='bank_data', lazy='dynamic')

    def __repr__(self):
        return self.name

    def get_args(self):
        return self.id, self.name


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    country_currency_bank_payment = db.relationship('CountryCurrencyBankPayment',
                                                    backref='payment_method', lazy='dynamic')

    def __repr__(self):
        return self.name

    def get_args(self):
        return self.id, self.name


class CountryCurrencyBankPayment(db.Model):
    __tablename__ = "country_currency_bank_payment"

    id = db.Column(db.Integer, primary_key=True)
    id_currency = db.Column(db.Integer, db.ForeignKey('currency.id'))
    id_country = db.Column(db.Integer, db.ForeignKey('country.id'))
    id_bank_data = db.Column(db.Integer, db.ForeignKey('bank_data.id'))
    id_payment_method = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    state = db.Column(db.Integer)

    def __repr__(self):
        return self.id

    def get_args(self):
        return (self.id, self.id_currency, self.id_country,
                self.id_bank_data, self.id_payment_method,
                self.state)
