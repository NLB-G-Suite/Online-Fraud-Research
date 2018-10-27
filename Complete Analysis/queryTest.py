import json

data = json.load(open('dataset.json'))

t = ''
for i in range(len(data['videoId'])):
	for j in data['linksUp'][i]:
		t += j+'\n'

with open('queries.txt','w') as f:
	f.write(t)
