# coding=utf8
import abc

from blitz.bw_env import bw_utils
from blitz.bw_env.bw_utils import get_bw_script

# Базовый класс для работы со скриптом на стороне сервера
class BWScriptBase(object):
    _SCRIPT_BASE_TEMPLATE = None
    PAYLOAD_PLACEHOLDER = '__INSERT__PAYLOAD__'

    def __init__(self):
        pass

    @abc.abstractmethod
    def process_name(self):
        """
        Возращаем имя процесса, на котором должен быть выполнен скрипт
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def internal_data(self, process_id):
        """
        Скрипт для выполенения

        :param process_id: Строковый идентификатор процесса, на котором будет выполняется скрипт.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def process_exe_result(self, result):
        """
        Обработать результат выполнение и вернуть истину, если обработка была успешной и требуется оснатновить обработку

        :param result: SSHCallResult объект
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def on_finished(self, processes):
        """
        Метод вызывается по завершению выполнения выполнения скриптов на всех процессах

        :param processes: Список процессов, на которых запускался скрипт
        """
        raise NotImplementedError()

    def data(self, process_id):
        """
        Непосредственно питоновский скрипт, уже в шаблонной обвязке

        :param process_id: Строковый идентификатор процесса, на котором будет выполняется скрипт.
        """
        return self._get_script_base_template().replace(BWScriptBase.PAYLOAD_PLACEHOLDER, self.internal_data(process_id))

    def _get_script_base_template(self):
        """
        Возвращает шаблон для скрипта
        """
        if BWScriptBase._SCRIPT_BASE_TEMPLATE is None:
            with open(get_bw_script('server_command_template/bw_base_template.py'), 'r') as f:
                BWScriptBase._SCRIPT_BASE_TEMPLATE = f.read()

        return BWScriptBase._SCRIPT_BASE_TEMPLATE

#
class BWServiceAppScript(BWScriptBase):
    """
    Для скриптов на стороне serviceapp
    """
    def __init__(self, pattern):
        self.pattern = pattern

    def process_name(self):
        return 'serviceapp'

    def internal_data(self, process_id):
        return self.pattern

    def process_exe_result(self, result):
        return False # execute on all processes

    def on_finished(self, processes):
        pass


class BWAccountScript(BWScriptBase):
    """
    Для скриптов аккаунта на baseapp
    """
    _SCRIPT_ACCOUNT_TEMPLATE = None
    MISSED_ENTITY_MARKER = '[MISSED ENTITY]'

    def __init__(self, pattern, dbid_list):
        self.pattern = pattern
        self.initial_dbid_list = dbid_list
        self.remaining_dbid_list = dbid_list

    def process_name(self):
        return 'baseapp'

    def internal_data(self, process_id):
        data = self._get_account_template().replace(BWScriptBase.PAYLOAD_PLACEHOLDER, self.pattern)
        data = data % {
            'dbid_list': self.remaining_dbid_list,
            'process_id': process_id,
        }

        return data

    def process_exe_result(self, result):
        self.remaining_dbid_list = bw_utils.get_data_by_marker(BWAccountScript.MISSED_ENTITY_MARKER, result.output)
        return self.remaining_dbid_list is None or len(self.remaining_dbid_list) == 0

    def on_finished(self, processes):
        if self.remaining_dbid_list:
            raise RuntimeError('Following account did\'t found {} on process {}'.format(self.remaining_dbid_list, processes))

    def _get_account_template(self):
        if BWAccountScript._SCRIPT_ACCOUNT_TEMPLATE is None:
            with open(get_bw_script('server_command_template/bw_base_account_command.py'), 'r') as f:
                BWAccountScript._SCRIPT_ACCOUNT_TEMPLATE = f.read()

        return BWAccountScript._SCRIPT_ACCOUNT_TEMPLATE


__all__ = [
    'BWServiceAppScript',
    'BWAccountScript',
]