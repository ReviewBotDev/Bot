import urlparse

class ConnectionConfig(object):
	#
	def __init__(self, scheme=None, username=None, password=None, hostname=None, port=None, path=None):
		self.scheme = scheme
		self.username = username
		self.password = password
		self.hostname = hostname
		self.port = int(port) if port is not None else None
		self.path = path
		self.deffered = False

	def asDict(self):
		return {
			'scheme': self.scheme,
			'username': self.username,
			'password': self.password,
			'hostname': self.hostname,
			'port': self.port,
			'path': self.path,
		}

	@staticmethod
	def fromURL(url):
		# urlparse in bigworld's python doesn't parse unknown schema
		urlsplit = url.split(':')
		real_scheme = urlsplit[0]
		urlsplit[0] = 'http'

		parsed = urlparse.urlparse(':'.join(urlsplit))
		config = {
			'scheme': real_scheme,
			'username': parsed.username,
			'password': parsed.password,
			'hostname': parsed.hostname,
			'port': parsed.port,
			'path': parsed.path
		}
		return ConnectionConfig(**config)
