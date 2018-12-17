# coding=utf8
# Здесь хранятся все геттеры на ресурсы игры

import os

from common.config import get_global_property
from project.constants import paths
from config_descr import NAME
from release_data import shared_data_helper

__all__ = [
    'ru_yaml_path',
    'camouflage_xml_path',
    'get_stuff_xml',
    'nation_list_xml_path',
    'get_regions_yaml_path',
    'get_vehicles',
    'get_account_types_xml',
]

def _get_item_defs():
    return paths.get_server_item_defs_dir(get_global_property(NAME.wbs_src_dir))


def ru_yaml_path():
    return os.path.join(paths.get_data_source_strings_dir(get_global_property(NAME.project_dir)), 'ru.yaml')


def camouflage_xml_path():
    return paths.get_camouflages_xml_path(_get_item_defs())


def get_stuff_xml():
    return paths.get_stuff_xml_path(_get_item_defs())


def nation_list_xml_path(nation):
    return os.path.join(get_global_property(NAME.vehicles_dir), nation, 'list.xml')


def get_regions_yaml_path():
    return os.path.join(get_global_property(NAME.data_source_dir), 'regions_development.yaml')


def get_vehicles():
    return shared_data_helper.get_tanks(get_global_property(NAME.vehicles_dir), get_global_property(NAME.resources_config))


def get_account_types_xml():
    return os.path.join(get_global_property(NAME.server_dir), 'scripts', 'server_xml', 'account_types.xml')
