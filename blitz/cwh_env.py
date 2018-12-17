# coding=utf8
import json

import requests

from toolcommon.logger import g_logger

CHECK_URL = 'http://{0}/wotb/accounts/?ids=1'
ADD_POINTS = 'http://{0}/wotb/points/'


def check(host):
    if not host:
        g_logger.error('Host is empty')
        return

    url = CHECK_URL.format(host)
    g_logger.info(url)
    try:
        response = requests.get(url, timeout=3)
        g_logger.debug(response.content)
        return response.ok
    except:
        g_logger.exception(url)
        return False


def get_admin_url(host):
    if host:
        return 'http://{}/admin/'.format(host)



def add_points(host, dbid, points):
    if not host:
        g_logger.error('Host is empty')
        return

    if not isinstance(dbid, (int, long)):
        g_logger.error('Wrong dbid')
        return

    url = ADD_POINTS.format(host)
    payload = {
        dbid: {'points': points},
    }
    response = requests.post(url, json=payload)

    g_logger.debug(response.content)

    content = json.loads(response.content)
    if not response.ok:
        reason = response.content
        if 'description' in content:
            reason = content['description']

        g_logger.warning('Points {0} wasn\'t added to {1} - {2}'.format(points, dbid, reason))
        return False

    g_logger.success('Points {0} was added to {1}'.format(points, dbid))
    return True
