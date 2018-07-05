import json

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
			flag = 0
			# for word in wordList:
			if (('\"ad\"' in ldaResults[1] or '\"ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
				temp.append(ldaResults[1])
				# flag += 1
			# if flag >= 2:
		if len(temp) > 1:
			fraudChannelsTitle[channels] = temp
	except Exception,e:
		print str(e) 

	try:
		temp = []

		for ldaResults in data[channels]["description"]:
			flag = 0
			if (('\"ad\"' in ldaResults[1] or '\"ad-' in ldaResults[1]) and 'click' in ldaResults[1]) or 'click' in ldaResults[1]:
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
		
with open('ldaOn_ad_clickTitles.json','w') as f:
	json.dump(fraudChannelsTitle,f)

with open('ldaOn_ad_clickDescription.json','w') as f:
	json.dump(fraudChannelsDescription,f)

with open('ldaOn_ad_clickTag.json','w') as f:
	json.dump(fraudChannelsTag,f)
