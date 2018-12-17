# coding=utf8
from copy import deepcopy
from collections import OrderedDict

from cluster.cluster_list import CLUSTERS, HOST, PORT, LOGIN, CENTER

from toolcommon.utils import cached_value


__all__ = [
    'HOST',
    'PORT',
    'LOGIN',
    'CENTER',
    'MQURL',
    'FAKE_LOCAL_SERVER',

    'is_production',
    'is_dev',
    'is_cluster',

    'get_clusters',
    'get_dev_clusters',
    'get_prod_clusters',
]

MQURL = 'mqurl'
FAKE_LOCAL_SERVER = 'fake_local'


_PRODUCTION_CLUSTERS = ['RU', 'EU', 'US', 'SG', 'CN1', 'ST30', 'ST31', 'ST32', 'TRUNK_DEV', 'wotblitz20']
_FAKE_PRODUCTION = ['TRUNK_DEV', 'wotblitz20']

_MQURL = {
    'TRUNK_DEV': 'amqp://mq-wotbwgs100:mq-wotbwgs100@ws-ovz-82.iv:5672/mq-wotbwgs100',
    'wotblitz20': 'amqp://mq-blitz2201:mq-blitz2201@by1-web-blitz-2:5672/mq-blitz2201',
    'LOCAL': 'amqp://mq-blitz2201:mq-blitz2201@by1-web-blitz-2:5672/mq-blitz2201',
    # prod
    'RU': 'amqp://mq-wotbru:mq-wotbru@mq-wotb-ru.wargaming.net:5672/mq-wotbru',
    'EU': 'amqp://mq-wotbeu:mq-wotbeu@mq-wotb-eu.wargaming.net:5672/mq-wotbeu',
    'US': 'amqp://mq-wotbus:mq-wotbus@mq-wotbus.wargaming.net:5672/mq-wotbus',
    'SG': 'amqp://mq-wotbsg:mq-wotbsg@mq-wotbsg.wargaming.net:5672/mq-wotbsg',
    'CN1': 'amqp://mq-wotblitzcn1:mq-wotblitzcn1@mq-wotblitzcn1.wdo.io:5672/mq-wotblitzcn1',
    'ST30': 'amqp://mq-wotbst30:mq-wotbst30@mq-st30.wdo.io:5672/mq-wotbst30',
    'ST31': 'amqp://mq-wotbst31:mq-wotbst31@mq-wotbst31.wdo.io:5672/mq-wotbst31',
    'ST32': 'amqp://mq-wotbst32:mq-wotbst32@mq-wotbst32.wdo.io:5672/mq-wotbst32',
}


def is_production(name, real_only=False):
    is_real = name not in _FAKE_PRODUCTION
    is_prod = name in _PRODUCTION_CLUSTERS

    if real_only:
        return is_real and is_prod

    return is_prod


def is_dev(name):
    return not is_production(name, True)


def is_cluster(name):
    return name in get_clusters()


@cached_value
def get_clusters():
    r = OrderedDict()
    for v in sorted(CLUSTERS.keys()):
        r[v] = deepcopy(CLUSTERS[v])

    r[FAKE_LOCAL_SERVER] = {
        HOST: 'local',
        PORT: 80,
    }

    r['CN1'] = {
        LOGIN: 'wotblitzbox',
        HOST: '192.168.50.50',
        PORT: 22001,
        CENTER: True,
    }

    for name, url in _MQURL.iteritems():
        r[name][MQURL] = url

    return r


@cached_value
def get_dev_clusters():
    r = OrderedDict()
    for k, v in get_clusters().iteritems():
        if is_dev(k):
            r[k] = v

    return r


@cached_value
def get_prod_clusters():
    r = OrderedDict()
    for k, v in get_clusters().iteritems():
        if is_production(k):
            r[k] = v

    return r


def get_dev_cluster(name):
    return get_dev_clusters().get(name, None)