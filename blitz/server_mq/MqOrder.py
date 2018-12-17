import time
import pickle
import random

import amqp as amqplib

from blitz.server_mq.ConnectionConfig import ConnectionConfig

MIN_ACC_MOVER_VERSION = 0
MAX_ACC_MOVER_VERSION = 1

class ACCOUNT_MOVE_REQUEST_TYPE:
	EXTRACT = 0
	UPLOAD = 1
	EXTRACT_RANDOM = 2
	ACCOUNTS_LOAD_UP = 3

class ACCOUNT_MOVE_REQUEST_STATUS:
	SUCCESS = 'success'
	ERROR = 'error'

MAX_ACCOUNTS_PER_REQUEST = 200

class MqOrder(object):
	def __init__(self, host, vhost, user, password, exchange):
		self.host = host
		self.user = user
		self.vhost = vhost
		self.password = password
		self.exchange = exchange


class MqOutputOrder(MqOrder):
	def __init__(self, host, vhost, user, password, exchange, routing_key):
		MqOrder.__init__( self,
			host = host,
			vhost = vhost,
			user = user,
			password = password,
			exchange = exchange
		)

		self.routing_key = routing_key
		self.content_type = 'application/x-pickle'
		self.delivery_mode = 2
		self.exchange_type = 'direct'

		self.messageType = random.randint(1, 1000000)
		self.__msgReceived = None

	def push(self, messageId, data):
		connection = amqplib.Connection(
			host = self.host,
			userid = self.user,
			password = self.password,
			virtual_host = self.vhost
		)

		channel = connection.channel()
		channel.exchange_declare(
			exchange=self.exchange,
			type=self.exchange_type,
			durable=True,
			auto_delete=False
		)

		msg = amqplib.Message(body=pickle.dumps(data), application_headers={
			'type': self.messageType,
			'id':  messageId,
		},
			delivery_mode=self.delivery_mode,
			content_type=self.content_type,
		    content_encoding = 'text/plain',
		)

		res = channel.basic_publish(
			exchange = self.exchange,
			routing_key = self.routing_key,
			msg=msg
		)

		connection.close()
		assert res


class MqInputOrder(MqOrder):
	def __init__(self, host, vhost, user, password, exchange, queue):
		MqOrder.__init__( self,
			host = host,
			vhost = vhost,
			user = user,
			password = password,
			exchange = exchange
		)

		self.queue = queue

	def waitAndPop(self, messageId, requeueOther = True, timeout = 15):
		timeOutTime = time.time() + timeout
		self.__expectedMessageId = messageId

		connection = amqplib.Connection(
			host = self.host,
			userid = self.user,
			password = self.password,
			virtual_host = self.vhost
		)

		channel = connection.channel()
		self.__channel = channel
		channel.exchange_declare(
			exchange=self.exchange,
			type='direct',
			durable=True,
			auto_delete=False
		)

		checked = []
		otherMessages = []

		while True:
			if time.time() > timeOutTime:
				raise Exception, 'timeout'

			msg = channel.basic_get(queue = self.queue, no_ack = False)
			if msg is None:
				time.sleep(1)
				continue

			if msg.headers['id'] == messageId:
				break

			checked.append(msg.headers['id'])
			otherMessages.append(msg)

		for otherMsg in otherMessages:
			overdue = float(msg.properties['application_headers']['deadline_at']) < time.time()
			if requeueOther and not overdue:
				channel.basic_reject(delivery_tag=otherMsg.delivery_tag, requeue=True)
			else:
				channel.basic_ack(delivery_tag=otherMsg.delivery_tag)

		channel.basic_ack(delivery_tag=msg.delivery_tag)
		connection.close()
		return pickle.loads(msg.body)


class AccountMoverRequestsMqOrder(MqOutputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqOutputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
		    routing_key = 'bigworld.acc_move_request'
		)

class AccountMoverAnswersMqOrder(MqInputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqInputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
		    queue = 'acc_move_response'
		    )

class AdminRequestsMqOrder(MqOutputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqOutputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
		    routing_key = 'bigworld.admin_request'
		)

class DynStuffRequestsMqOrder(MqOutputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqOutputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
		    routing_key = 'bigworld.dynamic_stuff_request'
		)

class DynStuffResponseMqOrder(MqInputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqInputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
		    queue = 'dynamic_stuff_response'
		    )

class ClassicTournamentMqOrder(MqOutputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqOutputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
			routing_key = 'bapi_request'
		)

class QuickTournamentMqOrder(MqOutputOrder):
	def __init__(self, url):
		conf = ConnectionConfig.fromURL(url)
		MqOutputOrder.__init__(
			self,
			host = conf.hostname + ':' + str(conf.port),
			vhost = conf.path,
			user = conf.username,
			password = conf.password,
			exchange = 'bigworld',
			routing_key = 'tms_qt_request'
		)
