import json

def potentialFraud():
	data = json.load(open('ldaonTitleDescriptionTagsResults.json'))
	tags = json.load(open('tagsDescriptionsTitleChannel.json'))

	fraudChannelsTitle = {}
	fraudChannelsDescription = {}
	fraudChannelsTag = {}

	wordList = ['click','scam','profit','profitclick','\"ad\"','\"ad-','fraud','clickbank','per','pay','adclick','probux','eas']
	for channels in data:
		try:
			temp = []
			for ldaResults in data[channels]["title"]:
				for word in wordList:
					if word in ldaResults[1]:
						temp.append(ldaResults[1])
			if len(temp) > 1:
				fraudChannelsTitle[channels] = temp
		except Exception,e:
			print str(e) 

		try:
			temp = []
			for ldaResults in data[channels]["description"]:
				for word in wordList:
					if word in ldaResults[1]:
						temp.append(ldaResults[1])
			if len(temp) > 1:
				fraudChannelsDescription[channels] = temp
		except Exception,e:
			print str(e)  

		try:
			temp = []
			for video in tags[channels]:
				for tag in tags[channels][video]['tags']:
					flag = 0
					for word in wordList:
						if word in tag:
							flag += 1
					if flag >= 3 and (video,tags[channels][video]['title']) not in temp:
						temp.append((video,tags[channels][video]['title']))
			if len(temp) > 1:
				fraudChannelsTag[channels] = temp
		except Exception,e:
			print str(e)
			
	with open('ldaOn_ad_clickTitlesBuffer.json','w') as f:
		json.dump(fraudChannelsTitle,f)

	with open('ldaOn_ad_clickDescriptionBuffer.json','w') as f:
		json.dump(fraudChannelsDescription,f)

	with open('ldaOn_ad_clickTagBuffer.json','w') as f:
		json.dump(fraudChannelsTag,f)
