# coding=utf8
import requests

from toolcommon.logger import g_logger

CHECK_URL = 'http://{0}/version/'


def check(host):
    if not host:
        g_logger.error('Host is empty')
        return

    url = CHECK_URL.format(host)
    g_logger.info(url)
    try:
        response = requests.get(url, timeout=3)
        g_logger.info(response.content)
        return response.ok
    except:
        g_logger.exception(url)
        return False


def get_admin_url(host):
    return  None

