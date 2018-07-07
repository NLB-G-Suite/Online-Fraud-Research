import json

titles = json.load(open('ldaOn_ad_clickTitles.json'))
descs = json.load(open('ldaOn_ad_clickDescription.json'))
tags = json.load(open('ldaOn_ad_clickTag.json'))

uniqueChan = []
countDict = {}
wordList = ['click','scam','profit click','profitclick','ad ',' ads',' ad ','advertis',' ad-','fraud','clickbank','per','pay','adclick']
data = json.load(open('tagsDescriptionsTitleChannel.json'))


for channel in titles:
	uniqueChan.append(channel)

for channel in descs:
	if channel not in uniqueChan:
		uniqueChan.append(channel)

for channel in tags:
	if channel not in uniqueChan:
		uniqueChan.append(channel)

for channels in uniqueChan:
	countDict[channels] = [0.0,[]]
	# for video in allChannelVideos[channel]:
	# 	if ((' Ad ' in video[0] or ' Ad-' in video[0] or' ad ' in video[0] or ' ad-' in video[0]) and ('Click' in video[0] or 'click' in video[0])) or 'Click' in video[0] or 'click' in video[0]:
	# 		countDict[channel] += 1.0
	try:
		flag = 0
		for video in data[channels]:
			for word in wordList:
				if word in data[channels][video]['title'].lower():
					flag += 1
			if flag >= 2:
				countDict[channels][0] += 1.0
				countDict[channels][1].append(video)
	except Exception,e:
		print str(e) 

	try:
		flag = 0
		for video in data[channels]:
			for word in wordList:
				if word in data[channels][video]['description'].lower():
					flag += 1
			if video not in countDict[channels][1] and flag >= 2:
				countDict[channels][0] += 1.0
				countDict[channels][1].append(video)
	except Exception,e:
		print str(e)  

	try:
		flag = 0
		for video in data[channels]:
			for word in wordList:
				if word in data[channels][video]['tags']:
					flag += 1
			if video not in countDict[channels][1] and flag >= 2:
				countDict[channels][0] += 1.0
				countDict[channels][1].append(video)
	except Exception,e:
		print str(e)

mainDict = {}
for channel in countDict:
	mainDict[channel] = (countDict[channel][0],len(data[channel]),(countDict[channel][0]/len(data[channel])) * 100)

with open('PercentageFraudPerUser.json', 'w') as f:
	json.dump(mainDict, f)
with open('fraudUserVideos.json', 'w') as f:
	json.dump(countDict, f)	

temp = 'Channel Hyperlink: (Fraudulent Videos, Total Videos, Percentage Fraudulent)\n\n'
for channel in mainDict:
	temp += 'https://www.youtube.com/channel/'+str(channel)+': '+str(mainDict[channel])+'\n'
with open('PercentageFraudPerUser.txt','w') as f:
	f.write(temp)
