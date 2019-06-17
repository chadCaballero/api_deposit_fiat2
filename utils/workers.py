from threading import Thread
from apps.auth.models import Logger
from apps import db
from logger.manager import Multilog
import json, sys

log = Multilog(__name__).getLogger()

# forma uno basado en clases
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
# logging.debug('prueba')


def insert(kw):
    try:
        db.session.add(Logger(**kw))
        db.session.commit()
        log.info(**kw)
        sys.exit()
    except Exception:
        db.session.rollback()
        log.error('Error in logger insert')
    finally:
        pass


def update(kw):
    db.session.add(Logger(**kw))
    db.session.commit()
    log.info(kw)
    sys.exit()


def register_logger(rekuest=None, response=None, system='APIDEPFIAT', mode='IN'):
    if mode == 'IN':
        if rekuest and response:
            dic = dict()
            dic['id_user'] = response['id_user'] if 'id_user' in response else 0
            dic['endpoint'] = rekuest.url
            dic['ip'] = rekuest.remote_addr
            dic['method'] = rekuest.method
            dic['requestData'] = None if rekuest.method == 'GET' else str(rekuest.json)
            dic['responseData'] = response['data'] if 'data' in response else None
            dic['userAgent'] = rekuest.headers.get('User-Agent')
            dic['os'] = rekuest.user_agent.platform
            dic['responseCode'] = response['code'] if 'code' in response else None
            dic['from_sys'] = system
            h = Thread(target=insert, args=(dic,))
            h.start()
        else:
            log.error('argument rekuest is None')
    elif mode == 'UP':
        if rekuest:
            dic = dict()
            dic['id_user'] = response['id_user'] if 'id_user' in response else 0
            dic['responseData'] = 'res'
            dic['responseCode'] = 201
            h = Thread(target=update, args=(dic,))
            h.start()
        else:
            log.error('argument rekuest and response are None')
    else:
        log.error('mode is no permissive')
