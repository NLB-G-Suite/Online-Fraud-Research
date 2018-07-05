import json

data = json.load(open('TagsDescLinks.json'))

for chan in data:
	print 'CHANNEL: ',chan
	for id in data[chan]:
		print 'ID: ',id
		try:
			for link in data[chan][id]['links']:
				print link
		except:
			continue