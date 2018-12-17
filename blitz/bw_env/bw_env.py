# coding=utf8
import os

from lxml import etree

from blitz import cluster_env
from blitz import file_location_env
from blitz import resources_env
from blitz.ssh_connection import SSHConnection
from blitz.bw_env.bw_utils import get_bw_script
from blitz.bw_env.bw_script import BWAccountScript, BWServiceAppScript
from blitz.bw_env import bw_utils
from blitz.external_deps import get_temp_path, get_cache_path
from blitz.external_deps import unix_path
from blitz.external_deps import fs
from blitz_v2 import server_env
from blitz_v2 import webstaging_env, spa_env
from cluster import cluster_manager
from cluster.cluster_list import HOST, PORT

from toolcommon.logger import g_logger
from toolcommon.utils import static_vars


__all__ = [
    'get_stuff_choices',
    'BWServer',
    'get_bw_server_object',
    'reset_bw_server_object',
]


def get_stuff_choices(server_name):
    try:
        bw = get_bw_server_object(server_name)
        local_path = bw.get_server_file('stuff.xml')
    except Exception as e:
        g_logger.exception('Cannot receive stuff.xml {}'.format(e))
        local_path = file_location_env.get_stuff_xml()

    return resources_env.get_stuff_choices(local_path)


class RemoteBWServerMixin(object):
    def remote_host(self):
        raise NotImplementedError()

    def remote_port(self):
        raise NotImplementedError()


class BWServer(RemoteBWServerMixin):
    def __init__(self, server_name):
        super(BWServer, self).__init__()

        self.script_runs = 0
        self.cluster_name = server_name
        self.ssh = None

        if cluster_env.is_production(server_name, True):
            g_logger.debug('SSH connection is not allowed for {0}'.format(server_name))
            self.bw_xml_path = None
            self.data = None
            return

        fs.recreate_empty_folder(get_temp_path(server_name))
        fs.recreate_empty_folder(get_cache_path(server_name))

        self.bw_xml_path = self.get_server_file('bw.xml')
        self.data = etree.parse(self.bw_xml_path) if self.bw_xml_path else None
        self.cluster = cluster_manager.Cluster(self.cluster_name)
        self._processes_by_name = {}

    # RemoteBWServerMixin
    def remote_host(self):
        return cluster_env.get_clusters()[self.cluster_name][HOST]

    def remote_port(self):
        return cluster_env.get_clusters()[self.cluster_name][PORT]

    def get_script_name(self):
        self.script_runs += 1
        index = self.script_runs % 10
        return '{cluster}_otool_run_script_{index}.py'.format(cluster=self.cluster_name, index=index)

    def __repr__(self):
        return '{0}: {1}'.format(self.__class__, self.cluster_name)

    def __get_value_from_xml(self, tag):
        if self.data is None:
            return None

        for node in self.data.findall("%s" % tag):
            if node.text:
                text = node.text.strip()
                if text:
                    return text

        return None

    def __get_host(self, tag):
        value = self.__get_value_from_xml(tag)
        if value is not None and value == 'localhost':
            return self.remote_host()

        return value

    def __get_mq_url(self, tag):
        value = self.__get_value_from_xml(tag)

        if value is not None:
            return value.replace('localhost', self.remote_host())

        return server_env.get_server_data(self.cluster_name).mqurl

    def get_realm(self):
        return webstaging_env.cast_server_to_realm(self.cluster_name)

    def get_dash_url(self):
        realm = self.get_realm()
        if realm:
            return "http://dash.wott.iv/?apps={realm}".format(realm=realm)

    def get_clan_api(self):
        return self.__get_host('wg/http_hosts/clan_api')

    def get_exporter_api(self):
        return self.__get_host('wg/http_hosts/exporter')

    def get_cwh_api(self):
        return self.__get_host('wg/http_hosts/cwh_api')

    def get_spa_api(self):
        return self.__get_host('wg/spa/host')

    def get_mq_url(self):
        return self.__get_mq_url('wg/mq_connections/connection/url')

    def get_server_console_logs(self):
        return 'http://{0}:8080/log/search'.format(self.remote_host())

    def is_xmpp_enabled(self):
        v = self.__get_value_from_xml('wg/xmpp/enabled')
        return v in ['1', 'true', 'True']

    def get_processes(self, ssh, process):
        if process not in self._processes_by_name or not self._processes_by_name[process]:
            result = ssh.execute('cluster-control | grep {}'.format(process))
            processes = bw_utils.get_processes(result.output, process)
            g_logger.info("Processes {} on {}".format(processes, self.cluster_name))

            if not processes:
                raise RuntimeError('Baseapps were missing {}'.format(self._processes_by_name))

            self._processes_by_name[process] = processes

        return self._processes_by_name[process]

    def get_server_file(self, file, use_cache=True):
        rule = {
            'cluster_profile.cfg': '~/.config/wotblitz2/cluster_profile.cfg',
            'bw.xml': '~/bw/res/wot/server/bw.xml',
            'stuff.xml': '~/bw/res/wot/scripts/item_defs/vehicles/common/stuff.xml',
        }

        path = rule[file] if file in rule else file

        local_path = get_cache_path(os.path.join(self.cluster_name, os.path.basename(path)))
        if not (fs.exists(local_path) and use_cache):
            with self.obtain_ssh_connection() as ssh:
                remote_path = unix_path(path)
                ssh.copy_from(remote_path, local_path)

        return local_path

    def _try_eval_script_on_processes(self, script):
        with self.obtain_ssh_connection() as ssh:
            processes = self.get_processes(ssh, script.process_name())
            for process in processes:
                need_stop = self._eval_script_on_specific_process(ssh, script, process)
                if need_stop:
                    break

            script.on_finished(processes)
            ssh.raise_if_errors_occurred()

        return True

    def _eval_script_on_specific_process(self, ssh, script, process_id):
        script_filename = self.get_script_name()
        filepath = get_temp_path(os.path.join(self.cluster_name, script_filename))
        with open(filepath, 'w+') as f:
            f.write(script.data(process_id))

        ssh.copy_to(filepath, script_filename)

        result = ssh.execute(u'cluster-control runscript {0} {1}; rm -rf {1}'.format(process_id, script_filename))
        return script.process_exe_result(result)

    def run_script_on_server_for(self, pattern, command):
        accs_dict = spa_env.get_dbid_dict_for_pattern(self.get_spa_api(), pattern)
        for acc_name, dbid in accs_dict.items():
            if dbid is None:
                g_logger.warning(u'Аккаунт {0} не найден! Проверьте корректность написания аккауна\шаблона аккаунтов'.format(acc_name))

        dbid_list = [dbid for dbid in accs_dict.values() if dbid is not None]
        if not dbid_list:
            g_logger.warning("Список найденных аккаунтов пуст!")
            return False

        script = BWAccountScript(command, dbid_list)
        return self._try_eval_script_on_processes(script)

    def send_notification_for(self, accPattern, notification):
        with open(get_bw_script('server_command_template/bw_send_wgnc_notification.py'), 'r') as f:
            cmd = f.read()

        cmd = cmd % {
            'notification': notification.replace('\n', '')
        }

        return self.run_script_on_server_for(accPattern, cmd)

    def run_script_on_serviceapp(self, cmd):
        return self._try_eval_script_on_processes(BWServiceAppScript(cmd))

    def obtain_ssh_connection(self):
        if self.ssh is None:
            self.ssh = SSHConnection(self.cluster_name)

        return self.ssh

    def reset_cache(self):
        reset_bw_server_object(self.cluster_name)


class BWFakeServer(BWServer):
    def __init__(self, *args, **kwargs):
        super(BWFakeServer, self).__init__(*args, **kwargs)

    # RemoteBWServerMixin
    def remote_host(self):
        return 'local'

    def remote_port(self):
        return 0

    # override
    def get_server_file(self, file, use_cache=True):
        rule = {
            'stuff.xml': file_location_env.get_stuff_xml(),
            'bw.xml': None
        }

        if file in rule:
            return rule[file]

        raise RuntimeError(file)


@static_vars(cache={})
def get_bw_server_object(server_name):
    if server_name not in get_bw_server_object.cache:
        if server_name is None or server_name == cluster_env.FAKE_LOCAL_SERVER:
            bw = BWFakeServer(cluster_env.FAKE_LOCAL_SERVER)
        else:
            bw = BWServer(server_name)

        get_bw_server_object.cache[server_name] = bw

    return get_bw_server_object.cache[server_name]


def reset_bw_server_object(server_name):
    if server_name in get_bw_server_object.cache:
        del get_bw_server_object.cache[server_name]

    return get_bw_server_object(server_name)
