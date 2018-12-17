# coding=utf8
import os

from toolcommon.utils import cached_value
from tank_xml.format.data_descr import g_nation_indexes
from tank_xml.vehicle.helper import make_compact_descr
from project.constants import CONFIG_CHOICES

from lxml import etree
import yaml

from toolcommon.logger import g_logger
from blitz import file_location_env

__all__ = [
    'get_localization',
    'localized',
    'get_stuff_choices',
    'get_camouflage_choices',
    'get_list_xml',
    'VehicleAggregatedData',
    'get_vehicle_data',
    'get_vehicle_data_by_fullname',
    'get_vehicles_choices',
    'get_configuration_modes',
    'get_configuration_modes_choices',
]

@cached_value
def get_localization():
    try:
        ru_yaml = file_location_env.ru_yaml_path()
        with open(ru_yaml, 'r') as f:
            return yaml.load(f)
    except:
        return {}


def localized(key):
    d = get_localization()
    return d.get(key, key)


#@cached_value Do not use cache for stuff xml
def get_stuff_choices(stuff_xml):
    data = etree.parse(stuff_xml)

    choices = []
    for node in data.findall("/*"):
        if node.find('purePrototype') is not None or node.tag == 'nextAvailableId':
            continue

        stuff_name = node.get('name', node.tag)
        stuff_id_node = node.find('id')
        stuff_id = None if stuff_id_node is None else int(stuff_id_node.text)
        loc_key = stuff_name

        titleStringNode = node.find('titleString')
        if titleStringNode is not None and titleStringNode.text is not None:
            loc_key = titleStringNode.text.strip()

        visibleName = u"{0} - {1} id {2}".format(localized(loc_key), stuff_name, stuff_id)
        choices.append((stuff_name, visibleName))

    choices = sorted(choices, key=lambda tup: tup[1])
    return choices


@cached_value
def get_camouflage_choices():
    data = etree.parse(file_location_env.camouflage_xml_path())

    choices = []
    for node in data.findall("/camouflages/*"):
        loc_key = node.tag

        userStringNode = node.find('userString')
        if userStringNode is not None and userStringNode.text is not None:
            loc_key = userStringNode.text.strip()

        idNode = node.find('id')
        if idNode is None or idNode.text is None:
            continue

        id = int(idNode.text.strip())
        name = localized(loc_key)
        vehicleNode = node.find('vehicleFilter/include/vehicle/name')
        if vehicleNode is not None and vehicleNode.text is not None:
            name = u'{0} - {1} ({2})'.format(name, vehicleNode.text.strip(), node.tag)
        else:
            name = u'{0} ({1})'.format(name, node.tag)

        choices.append((make_compact_descr('camouflage', 'none', id), name))

    choices = sorted(choices, key=lambda tup: tup[1])
    return choices


@cached_value
def get_list_xml(nation):
    list_xml = file_location_env.nation_list_xml_path(nation)

    if not os.path.isfile(list_xml):
        g_logger.warning("File not found: " + list_xml)
        return

    return etree.parse(list_xml)


class VehicleAggregatedData(object):
    def __init__(self, nation, name, vehicleNode):
        self.nation = nation
        self.name = name
        self.vehicle_id = int(vehicleNode.find('id').text.strip())
        self.nation_id = g_nation_indexes[nation]
        self.userString = vehicleNode.find('userString').text.strip()
        self.level = int(vehicleNode.find('level').text.strip())
        self.modes = vehicleNode.find('configurationModes').text.strip().split()

    def get_comp_descr(self):
        return make_compact_descr('vehicle', self.nation, self.vehicle_id)

    def get_fullname(self):
        return '{}:{}'.format(self.nation, self.name)

@cached_value
def get_vehicle_data(nation, vehicle):
    listData = get_list_xml(nation)
    vehicleNode = listData.find('/{0}'.format(vehicle))

    if vehicleNode is None:
        g_logger.warning('Vehicle {0}:{1} not found'.format(nation, vehicle))
        return None

    return VehicleAggregatedData(nation, vehicle, vehicleNode)


@cached_value
def get_vehicle_data_by_fullname(fullname):
    vdata = vehicles_data().get(fullname, None)
    if vdata is None:
        raise RuntimeError(compDescr)

    return vdata


def get_vehicles_choices(configurationModes=None):
    if configurationModes is None:
        configurationModes = get_configuration_modes()

    return __cached_get_vehicles_choices(frozenset(configurationModes))


@cached_value
def vehicles_data():
    vehicles = file_location_env.get_vehicles()

    vehicle_data = {}
    for n, l in vehicles.iteritems():
        for v in l:
            vdata = get_vehicle_data(n, v)

            if vdata is not None:
                vehicle_data[vdata.get_fullname()] = vdata

    return vehicle_data


@cached_value
def __cached_get_vehicles_choices(configurationModes):
    choices = []
    for fullname, vdata in vehicles_data().iteritems():
        if not (set(vdata.modes) & configurationModes):
            continue

        level = '10' if vdata.level == 10 else ' {0}'.format(vdata.level)
        uiString = u'{0}, {1} ур.: {2} ({3}) {4}'.format(vdata.nation, level, localized(vdata.userString), vdata.name, vdata.modes)
        choices.append((fullname, uiString))

    choices = sorted(choices, key=lambda tup: tup[1])
    return choices


@cached_value
def get_configuration_modes():
    return CONFIG_CHOICES


@cached_value
def get_configuration_modes_choices():
    return [(v, v) for v in get_configuration_modes()]


@cached_value
def get_server_account_types():
    return etree.parse(file_location_env.get_account_types_xml())
