from apps import db


class Logger(db.Model):
    __tablename__ = "log_deposit"

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    endpoint = db.Column(db.String(200))
    ip = db.Column(db.String(100))
    method = db.Column(db.String(6))
    requestData = db.Column(db.String(300))
    responseData = db.Column(db.String(800))
    userAgent = db.Column(db.String(200))
    os = db.Column(db.String(20))
    responseCode = db.Column(db.Integer)
    from_sys = db.Column(db.String(10))
    # createAt = db.Column(db.DateTime())  # valor por defecto en mysql
    # db.func.now()


class UserDetails(db.Model):
    __tablename__ = "userdetails"

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(50))
    emailid = db.Column(db.String(50))
    password = db.Column(db.String(255))
    profilepicture = db.Column(db.String(255))
    country = db.Column(db.Integer)
    state = db.Column(db.Integer)
    apiKey = db.Column(db.String(255))
    apiAccess = db.Column(db.String(111))
    keyname = db.Column(db.String(111))
    dateofreg = db.Column(db.Date)
    modified_date = db.Column(db.DateTime())
    timeofreg = db.Column(db.Time)
    status = db.Column(db.String(20))
    loginstatus = db.Column(db.String(111))
    activated_date = db.Column(db.Date)
    userip = db.Column(db.String(50))
    userbrowser = db.Column(db.String(200))
    randcode = db.Column(db.String(200))
    secret = db.Column(db.String(200))
    onecode = db.Column(db.String(200))
    url = db.Column(db.String(200))
    dninumber = db.Column(db.BigInteger)
    user_wallet = db.Column(db.String(255))
    xpub = db.Column(db.String(255))
    app_key = db.Column(db.String(255))
    app_key_tried = db.Column(db.Integer)
    app_key_status = db.Column(db.String(10))
    logintype = db.Column(db.String(30))
    # lastlogin = db.Column(db.DateTime())
    terms = db.Column(db.Integer)
    registeredfrom = db.Column(db.String(10))
    date_expiration = db.Column(db.Date)
    coins = db.Column(db.String(250))
    login_attempt = db.Column(db.Integer)
    date_attempt = db.Column(db.Date)
    sex = db.Column(db.String(1))
    profession = db.Column(db.String(255))
    municipality = db.Column(db.String(255))
    loginstatus_inka = db.Column(db.String(111))


class Login(object):
    # user_id = (int(), str())
    user_id = int()
    session_id = str()


class SubAdmin(db.Model):
    __tablename__ = "sub_admin"

    subId = db.Column(db.Integer, primary_key=True)
    sub_username = db.Column(db.String(111))
    sub_password = db.Column(db.String(111))
    permission = db.Column(db.String(111))
    status = db.Column(db.String(11))
