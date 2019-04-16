def curate_text(content):
	''' curate text content '''

	return content.encode('ascii','ignore').decode('utf-8') \
		if type(content) == str else content

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
