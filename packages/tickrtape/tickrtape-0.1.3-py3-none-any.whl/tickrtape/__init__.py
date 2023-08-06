__version__ = '0.1.0'

import requests
import json

CONTACT = 'http://167.172.29.122'

def pull(key, ticker, start, end):
	start = start.replace(' ', 'F')
	end = end.replace(' ', 'F')
	start = start.replace('-', 'Z')
	end = end.replace('-', 'Z')
	start = start.replace(':', 'A')
	end = end.replace(':', 'A')

	url = CONTACT + '/search/'

	conv = {'key' : key, 'ticker' : ticker, 'start' : start, 'end' : end}

	for x in conv.keys():
		if x != 'key':
			mid = '&{}={}'.format(x, conv[x])
		else:
			mid = '?{}={}'.format(x, conv[x])
		url += mid
	data = requests.get(url)
	data = data.text
	return json.loads(data)['results']

print(pull('beckettrotter@gmail.com', 'AAPL', '2013-05-05 00:00:00', '2013-05-08 00:00:00'))
