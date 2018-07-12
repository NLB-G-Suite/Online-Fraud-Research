import json
import csv 
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
				flagDict[video]['title'] = 'NoFlag'
				flagDict[video]['description'] = 'NoFlag'
				flagDict[video]['tags'] = 'NoFlag'
				wordFreq = {}
				for word in wordList:
					if word in data[channels][video]['title'].lower():
						flag +=1
					for tWord in data[channels][video]['title'].lower().split():
						if word in tWord:
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
					for dWord in data[channels][video]['description'].lower().split():
						if word in dWord:
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
				for word in wordList:
					check = 1
					for tag in data[channels][video]['tags']:
						if word in tag.lower():
							if check:
								flag +=1
								check = 0
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
				if len(countDict[channel][1][video]['description']) or len(countDict[channel][1][video]['tags']) or len(countDict[channel][1][video]['title']):
					cleanDict[channel][1][video] = countDict[channel][1][video]
	countDict = cleanDict

	mainDict = {}
	for channel in countDict:
		mainDict[channel] = (countDict[channel][0],len(data[channel]),(float(countDict[channel][0])/len(data[channel])) * 100)

	with open('PercentageFraudPerUserBuffer.json', 'w') as f:
		json.dump(mainDict, f)
	with open('fraudUserVideosBuffer.json', 'w') as f:
		json.dump(countDict, f)

	with open("FraudChannels.csv", "wb+") as file:
		f = csv.writer(file)
		f.writerow(
					['Channels',
					'FraudVideoCount',
					'Videos',
					'TitleFlag',
					'TagFlag',
					'DescriptionFlag'
				])

		for channel in countDict:
			check = 1
			for video in countDict[channel][1]:
				try:
					if check == 1:
						if 'title' in countDict[channel][1][video] and 'description' in countDict[channel][1][video] and 'tags' in countDict[channel][1][video]:
							f.writerow(
								['https://www.youtube.com/'+channel,
								countDict[channel][0],
								'https://www.youtube.com/watch?v='+video,
								countDict[channel][1][video]['title'],
								countDict[channel][1][video]['tags'],
								countDict[channel][1][video]['description']
							])
						check = 0
					else:
						if 'title' in countDict[channel][1][video] and 'description' in countDict[channel][1][video] and 'tags' in countDict[channel][1][video]:
							f.writerow(
								[' ',
								' ',
								'https://www.youtube.com/watch?v='+video,
								countDict[channel][1][video]['title'],
								countDict[channel][1][video]['tags'],
								countDict[channel][1][video]['description']
							])
				except Exception,e:
					print str(e)

	with open("PercentageFraudChannel.csv", "wb") as file:
		f = csv.writer(file)
		f.writerow([
			'Channel Hyperlink',
			'Fraudulent Videos',
			'Total Videos',
			'Percentage Fraudulent'
			])
		for channel in mainDict:
			f.writerow([
				'https://www.youtube.com/channel/'+channel,
				mainDict[channel][0],
				mainDict[channel][1],
				str(mainDict[channel][2])+'%'
			])

