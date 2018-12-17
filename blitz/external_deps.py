from jira import JIRAError
from jira import JIRA

from common.tempcache import get_temp_path, get_cache_path
from common.utils import unix_path

from internal.jira_api.config import JIRA_LOGIN, JIRA_SERVER
from internal import fs

from cluster import cluster_manager
from cluster.cluster_manager import SSHCallResult
from project.teamcity.enums import BuildBranchType


def get_password_by_login(login):
    # from internal.pmp.api import get_password_by_login
    JIRA_PASSWORD = 'beltaLowda1'  # get_password_by_login(JIRA_LOGIN)
    return JIRA_PASSWORD


__all__ = [
    'JIRAError',
    'JIRA',

    'JIRA_LOGIN',
    'get_password_by_login',
    'JIRA_SERVER',
    'fs',
    'unix_path',
    'get_temp_path',
    'get_cache_path',

    'cluster_manager',
    'SSHCallResult',
    'BuildBranchType',
]