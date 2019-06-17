from sqlalchemy import create_engine
from apps import app, db
import json
from utils.libs import dataset_to_dict, paginated_dict, fn_format_args, get_kwargs
from apps.auth.models import UserDetails, SubAdmin


# class Singleton:
#   def __init__(self, klass):
#     self.klass = klass
#     self.instance = None
#   def __call__(self, *args, **kwds):
#     if self.instance == None:
#       self.instance = self.klass(*args, **kwds)
#     return self.instance
#
#
# @Singleton
class Db:
    connection = None

    @staticmethod
    def get_connection():
        if Db.connection is None:
            Db.connection = db.session()
        return Db.connection

    def __enter__(self):
        # open the connection
        return self.connection.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        # close the connection
        self.connection.close()


def get_list_queryset_sp(sp_name=None, pagination=True, **kwargs):
    """
    :param sp_name:
    :param pagination:
    :param kwargs:
    :return:
    """
    try:
        if sp_name:
            dataset = db.session.execute(fn_format_args(sp_name, **kwargs))
            res = dataset_to_dict(dataset=dataset, pagination=pagination, **kwargs)
            return res
        else:
            return None
    except Exception:
        return None


def get_queryset_upsert_sp(sp_name=None, pagination=True, **kwargs):
    """
    :param sp_name:
    :param pagination:
    :param kwargs:
    :return:
    """
    try:
        if sp_name:
            dataset = Db.get_connection().execute(fn_format_args(sp_name, **kwargs))
            if dataset.returns_rows:
                Db.get_connection().flush()
                Db.get_connection().commit()
            res = dataset_to_dict(dataset=dataset, pagination=pagination, **kwargs)
            return res
        else:
            return None
    except Exception:
        db.session.rollback()
        return None


def check_user_session(user_id, status, session):
    try:
        res = UserDetails.query.filter_by(user_id=user_id, status=status, loginstatus_inka=session).count()
        return True if res > 0 else False
    except Exception:
        return False


def check_sub_admin(username, status, password, permission):
    try:
        res = SubAdmin.query.filter_by(sub_username=username, status=status, sub_password=password).first()
        if not res:
            return False
        if permission not in res.permission.split(','):
            return False
        return True
    except Exception:
        return False

# def check_user_session(*args):
#     try:
#         kwargs = get_kwargs(None, *args)
#         dataset = Db.get_connection().execute(fn_format_args('sp_validate_login', **kwargs))
#         # return dataset.returns_rows # bool
#         return True if dataset.fetchall()[0][0] > 0 else False
#     except Exception:
#         return False
