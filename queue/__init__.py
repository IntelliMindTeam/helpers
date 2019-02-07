import redis
import json

from connections import get_redis_connection

# Queue block secs
QUEUE_POP_TIMEOUT = 5

class RedisQueue(object):
	""" Simple Queue with Redis backend """

	def __init__(self, name, config, namespace='queue'):
		''' Initialize Queue '''

		self.key = '%s::%s' %(namespace, name)
		self.config = config

	def qsize(self):
		''' Return the approximate size of the queue. '''

		conn = get_redis_connection(self.config)
		return conn.llen(self.key)

	def empty(self):
		'''Return True if the queue is empty, False otherwise.'''	
	
		return self.qsize() == 0

	def push(self, value):
		''' Push an element to the tail of the queue '''

		conn = get_redis_connection(self.config)
		element = conn.lpush(self.key, json.dumps(value))
		return element

	def pop(self, block=True, timeout=QUEUE_POP_TIMEOUT):
		''' 
			Remove and return an item from the queue. 
        	If optional args block is true and timeout is None (the default), block
        	if necessary until an item is available 
		'''

		conn = get_redis_connection(self.config)
		popped_element = conn.brpop(self.key, timeout) if block else conn.lpop(self.key)

		if popped_element:
			return json.loads(popped_element[1])

		return None

	def pop_nowait(self):
		''' Equivalent to pop(False). '''
		return self.pop(False)


#users = RedisQueue('users')
