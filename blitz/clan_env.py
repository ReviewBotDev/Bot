# coding=utf8
import json
import random
import string

import requests

from toolcommon.logger import g_logger


CHECK_URL = 'http://{0}/clans/?fields=tag,name,id'
CREATE_URL = 'http://{0}/clans/'
MEMBERS_URL = 'http://{0}/v2/clans/{1}/members'
CREATE_APPLICATION = 'http://{0}//applications/'
GET_CLAN_BY_DBID = 'http://{0}/v2/accounts/{1}/profiles/wotb/?fields=clan.name,clan.tag,clan_id'
CLAN_URL = 'http://{0}/v2/clans/{1}'

NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 25

TAG_MIN_LENGTH = 2
TAG_MAX_LENGTH = 5


class ClanData(object):
    def __init__(self, json_response):
        self.clan_id = json_response.get('clan_id')
        self.name = json_response.get('clan', {}).get('name', None)
        self.tag = json_response.get('clan', {}).get('tag', None)


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
        return  'http://{}/admin/'.format(host)


def get_random_name_and_tag():
    def get_random_symbol():
        return random.choice(string.ascii_uppercase + string.digits)

    tagLength = random.randint(TAG_MAX_LENGTH, TAG_MAX_LENGTH) # always gen with maximum size
    tag = ''.join(get_random_symbol() for i in xrange(tagLength))

    tagLength = tagLength + 1 # underscore
    nameLength = random.randint(0 if tagLength > NAME_MIN_LENGTH else NAME_MIN_LENGTH - tagLength, NAME_MAX_LENGTH - tagLength)
    name = tag + '_' + ''.join(get_random_symbol() for i in xrange(nameLength))

    return name, tag


def __make_request(host, method, url, payload=None):
    if not host:
        g_logger.error('Host is empty')
        return

    response = getattr(requests, method)(url, json=payload, timeout=3)

    g_logger.debug(response.content)

    content = json.loads(response.content)
    if not response.ok:
        try:
            reason = response.content
            if 'description' in content:
                reason = content['description']
        except:
            pass

        g_logger.warning(u'Ошибка в запросе url {}, method {}, payload {}. Причина {}'.format(url, method, payload, reason))
        return None

    return content

def create_clan(host, clanName, clanTag, creator_dbid):
    url = CREATE_URL.format(host)
    payload = {
        'creator_id': creator_dbid,
        'name': clanName,
        'tag': clanTag,
        'motto': 'Default motto',
        'game': 'wotb',
        'game_data': {
            'emblem_preset_id': 10001
        }
    }
    content = __make_request(host, 'post', url, payload=payload)
    if content is None:
        return None

    g_logger.success('Clan {0}[{1}] created'.format(clanName, clanTag))
    return content['clan_id']


def add_members(host, clan_id, participants):
    url = MEMBERS_URL.format(host, clan_id)
    payload = {
        'ids': participants
    }
    content = __make_request(host, 'post', url, payload=payload)

    if content is None:
        return None

    g_logger.success(u'Игроки добавлены в клан {0}'.format(clan_id))
    return clan_id


def get_clan_info_for(host, dbid):
    if not isinstance(dbid, (int, long)):
        g_logger.error('Wrong dbid')
        return

    url = GET_CLAN_BY_DBID.format(host, dbid)
    content = __make_request(host, 'get', url)

    if content is None:
        return None

    clandata = ClanData(content)
    g_logger.success(u'Информация для игрока {0} о его клане {1}[{2}] получена'.format(dbid, clandata.name, clandata.tag))
    return clandata


def change_clan_emblem(host, clan_id, emblem_id):
    url = CLAN_URL.format(host, clan_id)
    payload = {
        'game_data': {
            'emblem_preset_id': emblem_id
        }
    }
    content = __make_request(host, 'patch', url, payload=payload)

    if content is None:
        return None

    g_logger.success(u'Эмблема клана (clanID:{0}) изменена на {1}'.format(clan_id, emblem_id))
    return True


def create_application(host, clan_id, sender_id):
    if not host:
        g_logger.error('Host is empty')
        return

    url = CREATE_APPLICATION.format(host)
    payload = {
        'clan_ids': [clan_id],
        'account_id': sender_id,
    }

    content = __make_request(host, 'post', url, payload=payload)

    if content is None:
        return None

    g_logger.success(u'Заявка для игрока {} создана в клан {}'.format(sender_id, clan_id))
    return True