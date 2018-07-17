import json

data = json.load(open('linkStatusBuffer.json'))
virusTotal = json.load(open('linkStatusBuffer.json'))

url = {}
for list in virusTotal.values():
	for dict in list:

		url[dict['resource']] = 