from functools import wraps
from helpers.log import get_logger

logger = get_logger('exception')

#......... Simple Generic Exception Handler Decorator .........#

def exception_handler(return_if_exception=None):
	''' decorator for generic exeption handling

		Params:
		* return_if_exception : it will be returned if any
								exeption occurs
	'''

	def real_decorator(method):

		@wraps(method)
		def wrapper(*args, **kargs):

			try:

				response = method(*args, **kargs)

			except Exception as ex:
				response = return_if_exception
				logger.error('Error in {}() func , args : {} {} :: {}'.format(\
					method.__name__, args, kargs, str(ex)))
			finally:
				return response

		return wrapper

	return real_decorator