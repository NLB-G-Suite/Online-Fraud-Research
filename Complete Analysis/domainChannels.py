import json

data1 = json.load(open('crawlerResultCheck.json'))

# uniqueVid=[]
# repeat=''
# print len(data1['videoId'])
# for i in range(len(data1['videoId'])):
# 	if data1['videoId'][i] not in uniqueVid:
# 		uniqueVid.append(data1['videoId'][i])
# 	else:
# 		repeat+=data1['videoId'][i]+'\n'

# with open('repeatVideos.txt','w') as f:
# 	f.write(repeat)

# print len(uniqueVid)

data1 = json.load(open('t1.json'))
data2 = json.load(open('t2.json'))
data3 = json.load(open('t3.json'))

dict={}
domains=json.load(open('filteredList.json'))
for domain in domains:
	for i in range(len(data1['videoId'])):
		for c in range(len(data1['linksUp'][i])):
			if data1['linksUp'][i][c]==domain:
				if data1['channelId'][i] not in dict:
					dict[data1['channelId'][i]]=[]
					if domain not in dict[data1['channelId'][i]]: 
						dict[data1['channelId'][i]].append(domain)

				else:
					if domain not in dict[data1['channelId'][i]]: 
						dict[data1['channelId'][i]].append(domain)

	for i in range(len(data2['videoId'])):
		for c in range(len(data2['linksUp'][i])):
			if data2['linksUp'][i][c]==domain:
				if data2['channelId'][i] not in dict:
					dict[data2['channelId'][i]]=[]
					if domain not in dict[data2['channelId'][i]]: 
						dict[data2['channelId'][i]].append(domain)

				else:
					if domain not in dict[data2['channelId'][i]]: 
						dict[data2['channelId'][i]].append(domain)

	for i in range(len(data3['videoId'])):
		for c in range(len(data3['linksUp'][i])):
			if data3['linksUp'][i][c]==domain:
				if data3['channelId'][i] not in dict:
					dict[data3['channelId'][i]]=[]
					if domain not in dict[data3['channelId'][i]]: 
						dict[data3['channelId'][i]].append(domain)

				else:
					if domain not in dict[data3['channelId'][i]]: 
						dict[data3['channelId'][i]].append(domain)
with open('domainChannels.json','w') as f:
	json.dump(dict,f)


