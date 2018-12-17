import logging

from blitz import CallstackLogger
from constants import BLITZTOOL_LOGGER_NAME, BLITZCLIENT_LOGGER_NAME

g_logger = None
g_client_logger = None

def setup():
    global g_logger
    global g_client_logger

    g_logger = logging.getLogger(BLITZTOOL_LOGGER_NAME)
    g_logger.setLevel(logging.DEBUG)
    g_client_logger = logging.getLogger(BLITZCLIENT_LOGGER_NAME)

    assert CallstackLogger == type(g_logger)
    assert CallstackLogger == type(g_client_logger)


__all__ = [
    'g_logger',
    'g_client_logger',
]