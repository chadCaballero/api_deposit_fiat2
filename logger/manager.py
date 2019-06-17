# -*- coding: UTF-8 -*-
import logging.handlers
import sys, os, platform
from apps.config import LOGGER_CONFIG


class Multilog:
    # clase que proporciona la funcionalidad de logging

    logger = None

    def __init__(self, log_name):
        """se inicializa la configuracion desde el archivo setting_secret.py y acorde al nombre enviado desde cada
           uno de los modulos que solicitan el manejador de logs"""
        log_folder = LOGGER_CONFIG['log_folder']
        log_file = LOGGER_CONFIG['files'][log_name] if log_name in LOGGER_CONFIG['files'] else LOGGER_CONFIG['files'][
            'error-dev']
        # rotate_time = LOGGER_CONFIG['rotate_time']
        log_level = LOGGER_CONFIG['log_level']
        log_count = LOGGER_CONFIG['log_count']
        log_format = LOGGER_CONFIG['log_format']
        log_maxsize = LOGGER_CONFIG['log_maxsize']
        log_mode = LOGGER_CONFIG['log_mode']

        # se obetiene la ruta a la carpeta de logs, verificando si esta en windows o unix
        if platform.platform().startswith('Windows'):
            FILE_PATH = os.path.join(os.getenv('HOMEDRIVE'),
                                     os.getenv("HOMEPATH"),
                                     log_folder,
                                     log_file)
        else:
            FILE_PATH = os.path.join(os.getenv('HOME'), log_folder, log_file)

        try:
            # obtener el logger correspondiente al modulo, ya implementa el patron singleton
            self.logger = logging.getLogger(log_name)
            # loggerHandler = logging.basicConfig(filename=FILE_PATH, filemode="a", format=LOG_FORMAT, level=log_level)
            # configuracion del handler para rotar por tamaño
            loggerHandler = logging.handlers.RotatingFileHandler(FILE_PATH, mode=log_mode, maxBytes=log_maxsize,
                                                                 backupCount=log_count, encoding=None, delay=0)
            # configuraicion del handler para rotar todos los dias a la medianoche
            # loggerHandler = logging.handlers.TimedRotatingFileHandler(FILE_PATH, rotate_time, 1, backupCount=LOG_COUNT)
            formatter = logging.Formatter(log_format)
            loggerHandler.setFormatter(formatter)
            self.logger.addHandler(loggerHandler)
            self.logger.setLevel(log_level)
        except Exception as error:
            print("Error with logs: %s" % (str(error)))
            sys.exit()

    def getLogger(self):
        # se obtiene el objeto "logger" para manejar todos los logs
        return self.logger
    # loggerMesage.critical('critical message')
    # loggerMesage.debug('debug message')
    # loggerMesage.exception("error")
