from functools import wraps
from helpers.log import get_logger

logger = get_logger('exception')

#......... Simple Decorator for Generic Exception Handler .........#

def exception_handler(return_if_exception=None):
	''' decorator for generic exeption handling

		Params:
		* return_if_exception : it will be returned if any
								exeption occurs o/w normal return
		e.g.
		----------------------------------------------------------
		# return empty list if any exception occur o/w normal flow

		@exception_handler(return_if_exception=[])
		def my_func(a, b):
			...
			...
		----------------------------------------------------------
		Note: If any exception occur during function run, it will be handled by
		this decorator, logged appropriately and
		return value as you specified in argument, (only if any exception)
		default will be None

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