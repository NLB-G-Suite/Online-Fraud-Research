import json

data = json.load(open('rawdata.json'))
tagsLinks = json.load(open('TagsDescLinks.json'))

for i in range(len(data['videoId'])):
	try:
		print tagsLinks[data['channelId'][i]][data['videoId'][i]]
		
		data['tags'] = tagsLinks[data['channelId'][i]][data['videoId'][i]]['tags']
		data['description'] = tagsLinks[data['channelId'][i]][data['videoId'][i]]['description']
		data['links'] = tagsLinks[data['channelId'][i]][data['videoId'][i]]['links']
	except Exception,e:
		continue

with open('buffer.json','w') as f:
	json.dump(data,f)