import json


def findPercentage():
	titles = json.load(open('ldaOn_ad_clickTitlesBuffer.json'))
	descs = json.load(open('ldaOn_ad_clickDescriptionBuffer.json'))
	tags = json.load(open('ldaOn_ad_clickTagBuffer.json'))

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
		countDict[channels] = [0,{}]
		flagDict = {}
		try:
			flag = 0
			for video in data[channels]:
				flagDict[video] = {}
				wordFreq = {}
				for word in wordList:
					if word in data[channels][video]['title'].lower():
						flag +=1
						if word in wordFreq:
							wordFreq[word] += 1
						else:
							wordFreq[word] = 1
				if len(wordFreq):
					flagDict[video]['title'] = wordFreq
				if flag >= 2:
					countDict[channels][0] += 1
		except Exception,e:
			print str(e) 
		try:
			flag = 0
			for video in data[channels]:
				wordFreq = {}
				for word in wordList:
					if word in data[channels][video]['description'].lower():
						flag +=1
						if word in wordFreq:
							wordFreq[word] += 1
						else:
							wordFreq[word] = 1
				if len(wordFreq):
					flagDict[video]['description'] = wordFreq
				if video not in flagDict and flag >= 2:
					countDict[channels][0] += 1
		except Exception,e:
			print str(e)
		try:
			flag = 0
			for video in data[channels]:
				wordFreq = {}
				for tag in data[channels][video]['tags']:
					for word in wordList:
						if word in tag.lower():
							flag +=1
							if word in wordFreq:
								wordFreq[word] += 1
							else:
								wordFreq[word] = 1
				if len(wordFreq):
					flagDict[video]['tags'] = wordFreq
				if video not in flagDict and flag >= 2:
					countDict[channels][0] += 1
		except Exception,e:
			print str(e)
		if len(flagDict):
			countDict[channels][1] = flagDict

	cleanDict = {}
	for channel in countDict:
		if countDict[channel][0] > 0:
			cleanDict[channel] = [0,{}]
			cleanDict[channel][0] = countDict[channel][0]
			for video in countDict[channel][1]:
				if len(countDict[channel][1][video]):
					cleanDict[channel][1][video] = countDict[channel][1][video]
	countDict = cleanDict

	mainDict = {}
	for channel in countDict:
		mainDict[channel] = (countDict[channel][0],len(data[channel]),(float(countDict[channel][0])/len(data[channel])) * 100)

	with open('PercentageFraudPerUserBuffer.json', 'w') as f:
		json.dump(mainDict, f)
	with open('fraudUserVideosBuffer.json', 'w') as f:
		json.dump(countDict, f)	

	temp = 'Channel Hyperlink: (Fraudulent Videos, Total Videos, Percentage Fraudulent)\n\n'
	for channel in mainDict:
		temp += 'https://www.youtube.com/channel/'+str(channel)+': '+str(mainDict[channel])+'\n'
	with open('PercentageFraudPerUserBuffer.txt','w') as f:
		f.write(temp)
