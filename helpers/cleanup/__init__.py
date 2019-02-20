
def cleanup_text(message):
	''' clean-up text '''

	try:
		message = message.decode('utf-8')
	except:
		try:
			message = message.decode('ISO-8859-1')
		except:
			try:
				message = message.decode('windows-1252')
			except:
				message = None

	return message
