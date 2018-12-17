# coding=utf8
"""
Пакет содержит модули, которые содержат зависимости на модули из игрового клиента.

Весь код, который использует клиентские скприты должны быть только здесь
"""
import os
import logging
import sys
import traceback

from constants import BLITZCLIENT_LOGGER_NAME, CLIENT_SCRIPTS_DIR

if CLIENT_SCRIPTS_DIR not in sys.path:
    sys.path.append(CLIENT_SCRIPTS_DIR)

from common.shared_logger import set_default_logger
from common.logger_class import SuccessLogger
from common.config import override_global_property, get_global_property
from config_descr.NAME import item_defs_dir, vehicles_dir, server_dir
from config_descr.PROJECT import g_section_name


class CallstackLogger(SuccessLogger):
    def __init__(self, *args, **kwargs):
        super(CallstackLogger, self).__init__(*args, **kwargs)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        record =  super(CallstackLogger, self).makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra)

        if level >= logging.ERROR and exc_info is None:
            try:
                raise ZeroDivisionError
            except ZeroDivisionError:
                f = sys.exc_info()[2].tb_frame.f_back.f_back.f_back

            record.exc_text = "".join(traceback.format_stack(f=f, limit=15))

        return record


def abs_path(rel):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), rel))


def setup_client():
    try:
        logging.setLoggerClass(CallstackLogger)

        logger = logging.getLogger(BLITZCLIENT_LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        set_default_logger(logger)

        logging.setLoggerClass(CallstackLogger) # do it again

        override_global_property(item_defs_dir, os.path.join(get_global_property(server_dir), 'scripts', 'item_defs'), g_section_name)
        override_global_property(vehicles_dir, os.path.join(get_global_property(server_dir), 'scripts', 'item_defs', 'vehicles'),
                                 g_section_name)
    except:
        print 'update blitz client local repository'


setup_client()