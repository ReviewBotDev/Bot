import logging

from blitz.external_deps import cluster_manager, unix_path

from toolcommon.logger import g_client_logger


class BWServerConsoleExceptionHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
        self.exceptions = []

    def emit(self, record):
        msg = record.getMessage()
        if msg.find('[ERROR]') != -1 or msg.find('ERROR:') != -1:
            self.exceptions.append(msg)


class SSHConnection(object):
    def __init__(self, cluster_name):
        self.cluster_name = cluster_name
        self.ssh = None
        self.exceptionHandler = None
        self.lock = 0

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def open(self):
        if self.lock == 0:
            self.exceptionHandler = BWServerConsoleExceptionHandler()
            self.user, self.host, self.port = cluster_manager.parse_user_host_port(self.cluster_name)

            localDomain = '.corp.wargaming.local'
            if self.host.find(localDomain) == -1:
                self.host = self.host + localDomain
            self.ssh = cluster_manager.get_ssh_client(self.user, self.host, self.port)

        self.lock += 1

    def close(self):
        self.lock -= 1

        if self.lock == 0 and self.ssh is not None:
            self.ssh.close()
            self.ssh = None
            self.exceptionHandler = None

    def _add_handler(self):
        g_client_logger.addHandler(self.exceptionHandler)

    def _remote_handler(self):
        g_client_logger.removeHandler(self.exceptionHandler)

    def copy_to(self, local_path, remote_path):
        remote_path = unix_path(cluster_manager.resolve_remote_path(remote_path, self.user))
        try:
            self._add_handler()
            return cluster_manager.ssh_copy_to(self.ssh, local_path, remote_path)
        finally:
            self._remote_handler()

    def copy_from(self, remote_path, local_path):
        try:
            self._add_handler()
            remote_path = unix_path(cluster_manager.resolve_remote_path(remote_path, self.user))
            return cluster_manager.ssh_copy_from(self.ssh, remote_path, local_path)
        finally:
            self._remote_handler()

    def execute(self, command, *args, **kwargs):
        try:
            self._add_handler()
            return cluster_manager.ssh_command(self.ssh, command, *args, **kwargs)
        finally:
            self._remote_handler()

    def raise_if_errors_occurred(self):
        if self.exceptionHandler.exceptions:
            raise RuntimeError(self.exceptionHandler.exceptions)

__all__ = [
    'SSHConnection',
]